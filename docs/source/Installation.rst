Installation
============

Placeholder.

Requirements
------------

Have the following installed on your system before installing MetaFunPrimer. The versions indicated are the versions that have been tested and confirmed to be working for this pipeline.

* CD-HIT (v4.6.8)
* Diamond (v0.9.14)
* Clustal Omega (v1.2.4)
* BLAST (v2.7.1+)
* EcoFunPrimer

To test if your installation is working, do the following:

.. code:: bash

    MetaFunPrimer -i test -m test_dir

Quickstart
----------

To get started, enter:

.. code:: bash

    MetaFunPrimer -i target_seqs -m metags

The inputs are as follows:

**target_seqs**
    A fasta file of the sequences of interest.

**metags**
    A directory of metagenomes (fasta files) representing the environment of study 
        
