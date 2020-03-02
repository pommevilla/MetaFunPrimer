Installation
============

**Note**: *MetaFunPrimer is currently in development and has only been tested on Michigan State University's ICER computing clusters. See the requirements below to see if you are able to run MetaFunPrimer on your system*. 

To install, begin by cloning the tools:

.. code:: bash

    $ git clone https://github.com/pommevilla/MetaFunPrimer.git

Then add ``MetaFunPrimer/src`` to your path by adding the following line to your ``bash_profile`` (or ``bashrc``) file:

.. code:: bash
    
    $ export PATH=$PATH:path/to/MetaFunPrimer/src

Finally, run ``check_reqs.sh`` to verify that that the required packages are installed and accessible to the pipeline:

.. code:: bash

    $ check_reqs.sh
    MetaFunPrimer
    =============
    Checking if required programs are installed and executable.
    
    Checking diamond: OK.
    Checking python: OK.
    Checking blastx: OK.
    Checking cd-hit: OK.
    Checking clustalo-1.2.4-Ubuntu-x86_64: OK.
    Checking parallel: OK.
    Checking qsub: OK.

    All required packages found. MetaFunPrimer is ready for use.
    See https://metafunprimer.readthedocs.io/en/latest/Tutorial.html for an introduction to the package.


Requirements
------------

Have the following installed on your system before installing MetaFunPrimer. The versions indicated are the versions that have been tested and confirmed to be working for this pipeline.

* `CD-HIT (v4.6.8) <http://weizhongli-lab.org/cd-hit/>`_
* `Diamond (v0.9.14) <https://github.com/bbuchfink/diamond>`_
* `Clustal Omega (v1.2.4) <http://www.clustal.org/omega/>`_
* `BLAST (v2.9.1+) <https://www.ncbi.nlm.nih.gov/books/NBK279671/>`_
* `Parallel <https://www.gnu.org/software/parallel/>`_
* `EcoFunPrimer <https://github.com/rdpstaff/EcoFunPrimer>`_

