Documentation
=============

``mfpcluster``
--------------

``mfpcluster`` clusters the sequences of a fasta file over a range of similarity values using `CD-HIT <http://weizhongli-lab.org/cd-hit/>`_. 

* **Inputs**
    
   * **-i, --in [input_fasta]**

        The fasta file to cluster. 

* **Outputs**

    * A directory containing:

        * *0.n.fa.clstr*: The clusters found by ``CD-HIT`` when clustering ``input_fasta`` at similarity threhsold *n*.
        * *0.n.fa*: Fasta files containing the representative sequences for the clusters found when clustering ``input_fasta`` at similarity threshold *n*. 
        * *<input_fasta>.log*: A plain-text document containing diagnostic information from the current run of ``mfpcluster``.
        * *command.cluster.sh*: A newline separated document containing the commands passed to `CD-HIT` to perform clustering.
        * *cluster_counts.tsv*: A tsv containing with columns for the similarity threshold clustered at, the number of clusters found at that simlarity threshold, and the first-order difference calculated at that point.

* **Optional arguments**

    * **-o, --out [string]** *(Default: <input_fasta>.clustering)* 
        
        The name of the output directory. 

Version History
---------------

* v0.51 (11/14/2019): Adding documentation.
* v0.5 (11/14/2019): Beta release.

