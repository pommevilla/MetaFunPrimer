MetaFunPrimer: qPCR primer design pipeline to target function
=============================================================

**MetaFunPrimer** is a primer design pipeline designed to target genes and functions within an environment. 

1. **mfpcluster**: The input genes are clustered using **CD-Hit**. A similarity level is recommended.
2. **mfpsearch**: Searches for the input genes against reference files.
3. **mfpcount**: Summarizes the results of **mfpsearch** by counting the presence and abundance of the input genes in the reference files. **mfpcount** will also recommend which clusters to include in the final primer design process.
4. **mfpprepare**: Formats and prepares a fasta file for input into the next step.
5. **mfpdesign**: Primers are designed using **EcoFunPrimer**. 
6. **mfpqpcr**: Performs `in silico` qPCR to determine primer effectiveness and specificity.  

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
