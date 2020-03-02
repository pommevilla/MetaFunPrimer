Tutorial 
========

This gives an example of what a basic workflow using MetaFunPrimer may look like. Included with the pipeline in the ``tests/test_data/rpoB_sample_data`` directory are three files:

    * ``rpoB.protein.fasta``, a nucleotide fasta file,
    * ``rpoB.nucleotide.fasta``, the protein fasta file for the above nucleotide sequences,
    * ``rpoB.nucleotide_protein_map.tsv``, a TSV file with the corresponding nucleotide sequence name for each protein sequence in the fasta file above. To be specific, the first column is the protein sequence identifier and the second column contains the nucleotide sequence identifier.

These are the three files necessary to run the pipeline.

The tutorial assumes that you were able to successfully run ``check_reqs.sh`` and received the "All required packages found" message. See the `Installation <https://metafunprimer.readthedocs.io/en/latest/Installation.html>`_ page for more info.

Determining optimal clustering threshold: ``mfpcluster``
--------------------------------------------------------

The first step in the ``MetaFunPrimer`` pipeline is to use `CD-HIT <http://weizhongli-lab.org/cd-hit/>`_ to determine an optimal similarity threshold for gene clustering. In order to do that, the ``mfpcluster`` function clusters the input sequence at every whole percent between 80% and 100%. It then recommends a similarity threshold to cluster at based on the `first-order difference <https://pommevilla.github.io/random/elbows.html>`_ of the number of gene clusters found.

We run ``mfpcluster`` from within the ``.../tests/test_data/rpoB_sample_data`` directory: 

.. code:: bash

    $ mfpcluster -i rpoB.protein.fasta
    Input file: rpoB.protein.fasta
    Output directory: rpoB.protein.fasta.clustering
    Beginning clustering...
    Clustering done.

    Getting cluster counts by similarity threshold > cluster_counts.tsv
    Calculating first-order differences > cluster_counts.tsv
    Optimum percentage (as calculated by first-order difference): 0.82
    Number of clusters: 24

After successfully running the command, the directory ``rpoB.protein.fasta.clustering`` is created, which contains:

    * ``rpoB.protein.fasta.log``, a text document containing the recommended similarity threshold and a suggestion for the next command to run in the pipeline
    * ``cluster_counts.tsv``, a tsv whose columns are the similarity threshold for clustering, the number of clusters found when clustering at that threshold, and the first-order difference of the cluster counts at calculated at that similarity threshold
    * ``command.cluster.sh``, the commands used to run the clustering commands
    * ``0.xx.fa.clstr``, one of the outputs of ``CD-HIT``, which shows the clusters found at similarity threshold *0.xx*. The representative gene of each cluster is indicated by a \*
    * ``0.xx.fa``, the other output of ``CD-HIT``, which contains the protein sequence of the representative genes found in ``0.xx.fa.clstr``

When we open ``rpoB.protein.fasta.log``, we see that the recommended similarity threshold is *0.82*, which results in 24 gene clusters. The recommended next command is ``mfpsearch -i 0.82.fa -e ../sample_metagenomes``. If the recommended similarity threshold results in too many or too few clusters, the user can consult ``cluster_counts.tsv`` and choose another threshold of their choice, modifying the ``mfpsearch`` command above accordingly.

Counting presence and abundance: ``mfpsearch``
-------------------------------------------------

The next step in the pipeline is to use ``mfpsearch`` to  quantify the presence and abundance of the gene clusters chosen in the previous step within the environmental metagenomes. Here, the `presence` of a gene is the number of samples it was found in, while its `abundance` is the total number of times the gene was found. We run the following command:

.. code:: bash

    $ mfpsearch -i 0.82.fa -e ../sample_metagenomes

``mfpsearch`` creates a `Diamond  <https://github.com/bbuchfink/diamond>`_ database from the input fasta file and performs a reverse search of the environmental metagenomes against this database. After successfully running the command, the directory ``0.82.fa.diamond_results`` is created, which contains:

    * ``0.82.fa.dmnd``, the Diamond database created by ``mfpsearch``
    * ``diamond_commands``, a directory containing:
        * ``commands.diamond.txt``, a file containing all of the individual diamond commands to be executed
        * ``job.diamond.xxx.sb``, a slurm job script containing a chunk of 20 lines of ``commands.diamond.txt``
        * ``job.checklist.tsv``, a tsv containing information about the status of all of the ``job.diamond.xxx.sb`` files.
    * ``<metagenome_file>.m8``, the results of the Diamond search against ``<metagenome_file>``

``mfpsearch`` automatically submits all of the Diamond jobs for the user using some preset job request parameters. However, this will use the default, general queue for job submissions. If you have access to a buy-in account, it is recommended to edit the ``/src/job_header`` file and adding the appropriate argument on line 14, just below the ``$SBATCH --mem-per-cpu=16G`` line. For example, if your account is ``<hpc_account>``, add the following line to ``job_header``:


.. code:: bash

    #SBATCH -A <hpc_account>

The ``job.checklist.tsv`` file contains information about each job that has been submitted. In particular, it indicates when that particular job has been submitted, started, and finished. Note, however, that just because a job will be listed as "finished" in ``job.checklist.tsv`` even if it terminates due to some error or timeout. It is suggested that one does a cursory glance over ``job.checklist.tsv`` or the individual result files (via ``wc -l *.m8``) to determine if this is the case. If so, we suggest that you manually resubmit the jobs after modifying the file accordingly (commenting out Diamond searches that have been successfully completed, modifying the job submission parameters).

Determining environmentally representative genes: ``mfpcount``
--------------------------------------------------------------

The next step in the process is to summarize the Diamond blast results and to determine which gene clusters are the most representative of the environment of study. This is done by counting the presence and abundance of each gene cluster, and then determining which clusters are overly represented using the *representation score*.

The representation score is attempts to 

.. code:: bash

    $ mfpcount -i 0.82.fa.diamond.result 

This command will create the following files:

    * ``0.96.fa.diamond_results.summary.tsv``, a TSV whose columns are
        * Gene name
        * Presence
        * Abundance
        * Representation score
        * Cumulative (normalized) representation score when the genes are ordered by representation score
        * First order difference of gene inclusion when ordered by gene abundance
        * Cumulative (normalized) abundance when genes are ordered by abundance 
    * ``0.96.fa.diamond_results.recommended_clusters.fo_diffs``, a list of gene recommended gene clusters for inclusion based on first-order differences. The recommendation is made in the following way:
        * Order the genes by abundance
        * Calculate the first order difference of each gene
        * Determine which gene has the highest first order difference score
        * Starting from the gene with the highest abundance, include every gene cluster until you hit the gene cluster with the highest first-order difference
    * ``0.96.fa.diamond_results.recommended_clusters.s_score``, a list of gene clusters recommended for inclusion based on the representation score. The recommendation is made in the following way:
        * Separately normalize the presence and abundance of each gene to be between 0 and 100.
        * Calculate the mean of the new normalized presence and abundance to get the *representation score* (R-score)
        * Reorder the genes by the R-score and calculate the cumulative R-score
        * Include genes until you meet some cumulative R-score threshold. By default this inclusion threshold is 0.80, though the user can set this to be whatever they choose
    * ``0.96.fa.diamond_results.log``, which contains details about the run of ``mfpcount``

Preparing fasta files for primer design: ``mfpprepare``
-------------------------------------------------------

Now that we have summarized the results and determined which clusters to include, we now prepare the fasta files for input into `EcoFunPrimer <https://github.com/rdpstaff/EcoFunPrimer>`_. The command prepares and submits a job submission that will peform the following actions:

   * Finds the nucleotide sequences corresponding to the protein sequecnes to be included (as indicated by the inclusion file)
   * Aligns them using `Clustal Omega (v1.2.4) <http://www.clustal.org/omega/>`_
   * Removes any *N* characters from this aligned file


The code to run this is

.. code:: bash

    $ mfpprepare -n fungene_9.6_amoA_AOB_1205_unaligned_nucleotide_seqs.fa -p fungene_9.6_amoA_AOB_1205_unaligned_protein_seqs.fa -c fungene_9.6_amoA_AOB_1205_unaligned_protein_seqs.fa.clustering/0.96.fa.clstr -t fungene_9.6_amoA_AOB_1205_unaligned_protein_seqs.fa.clustering/0.96.fa.diamond_results.recommended_clusters.s_score -m proteinTransNameNucleotide.txt


Here is an explanation of each of the arguments:

    * ``-n`` is the nucleotide fasta file
    * ``-p`` is the protein fasta file
    * ``-c`` is the cluster information file (output from ``CD-HIT`` in the ``mfpcluster`` step)
    * ``-t`` is the thresholding file, containing the names of the clusters to include for primer design. Examples of these files are the ``0.96.fa.diamond_results.recommended_clusters.s_score`` and ``0.96.fa.diamond_results.recommended_clusters.fo_diffs`` files output in the previous steps. 
    * ``-m`` is the protein-nucleotide sequence map  

Notes:

    * The thresholding files output by ``mfpcount`` are only suggestions. If desired, the user can supply their threshold file by writing the names of each desired gene cluster in a newline-separated text document (see the ``*.recommended_clusters.*`` files for examples). You can then pass this file as the argument to the `-t` paramater above. 

Designing primers: ``mfpdesign``
--------------------------------

Now that the files have been prepared for use, we will now use the ``mfpdesign`` command to submit a job to calculate primers.

.. code:: bash

    $ mfpdesign -i prepped.rpoB.fa

Some output will flash on the screen and you will see that a job has been submitted.

This command will create the following files:

    * ``0.82.fa.dmnd``, the Diamond database created by ``mfpsearch``
    * ``diamond_commands``, a directory containing:
        * ``commands.diamond.txt``, a file containing all of the individual diamond commands to be executed
        * ``job.diamond.xxx.sb``, a slurm job script containing a chunk of 20 lines of ``commands.diamond.txt``
        * ``job.checklist.tsv``, a tsv containing information about the status of all of the ``job.diamond.xxx.sb`` files.
    * ``<metagenome_file>.m8``, the results of the Diamond search against ``<metagenome_file>``


