MetaFunPrimer: qPCR primer design pipeline to target function
=============================================================

**MetaFunPrimer** is a primer design pipeline designed to target genes and functions within an environment. The inputs to MetaFunPrimer are a (nucleotide or protein) fasta file of the genes of interest and a directory containing metagenomes files representing the environment of study. MetaFunPrimer then performs the following steps; 

1. **Cluster**: The input genes are clustered using **CD-Hit**.
2. **Filter**: MetaFunPrimer determines which genes are abundant within the environment of interest by performing **DIAMOND-BLAST** with the representative sequences of the clusters found in the Cluster step against the metagenome files provided as input.
3. **Design**: Primers are designed for the environmentally abundant genes identified in the Filter step using the **EcoFunPrimer**. 

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   Installation
   Tutorial
   Documentation
   Support
   License


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
