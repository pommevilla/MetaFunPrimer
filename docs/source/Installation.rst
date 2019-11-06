Installation
============

**Note**: *MetaFunPrimer is currently in development and has only been tested on Michigan State University's ICER computing clusters. See the requirements below to see if you are able to run MetaFunPrimer on your system*. 

To install, begin by cloning the tools:

.. code:: bash

    git clone https://github.com/pommevilla/MetaFunPrimer.git

Then add `MetaFunPrimer/src` to your path by adding the following line to your bash_profile (or bashrc) file:

.. code:: bash
    
    export PATH=$PATH:path/to/MetaFunPrimer/src


Requirements
------------

Have the following installed on your system before installing MetaFunPrimer. The versions indicated are the versions that have been tested and confirmed to be working for this pipeline.

* `CD-HIT (v4.6.8) <http://weizhongli-lab.org/cd-hit/>`_
* `Diamond (v0.9.14) <https://github.com/bbuchfink/diamond>`_
* `Clustal Omega (v1.2.4) <http://www.clustal.org/omega/>`_
* `BLAST (v2.9.1+) <https://www.ncbi.nlm.nih.gov/books/NBK279671/>`_
* `EcoFunPrimer <https://github.com/rdpstaff/EcoFunPrimer>`_



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
        
