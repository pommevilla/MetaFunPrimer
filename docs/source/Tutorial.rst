Tutorial 
========

This gives an example of what a basic workflow using MetaFunPrimer may look like. Included with the pipeline in the ``tests/test_data/rpoB_sample_data`` directory are three files:

    * ``rpoB.protein.fasta``, a nucleotide fasta file,
    * ``rpoB.nucleotide.fasta``, a protein fasta file,
    * ``rpoB.nucleotide_protein_map.tsv``, a TSV file showing the corresponding nucleotide sequence name for each protein sequence in the fasta file above

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

When we open ``rpoB.protein.fasta.log``, we see that the recommended similarity threshold is *0.82*, which results in 24 gene clusters. The recommended next command is ``mfpsearch -i 0.82.fa -e ../sample_metagenomes``.  

If the recommended similarity threshold results in too many or too few clusters, the user can consult ``cluster_counts.tsv`` and choose another threshold of their choice, modifying the ``mfpsearch`` command above accordingly.

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

Determining environmentally representative genes: ``mfpcount``
--------------------------------------------------------------

The next step in the process is to summarize the Diamond blast results and to determine which gene clusters are the most representative of the environment of study. This is done by counting the presence and abundance of each gene cluster, and then determining which clusters are overly represented using the *representation score*.

Preparing fasta files for primer design: ``mfpprepare``
-------------------------------------------------------

Designing primers: ``mfpdesign``
--------------------------------

In-silico qPCR: ``mfpqpcr``
---------------------------
