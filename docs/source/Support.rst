Troubleshooting and Support
===========================

``MetaFunPrimer`` is still in active development. 

If you run into any problems or have any questions, check to see if it has been answered below. If not, submit an issue on the `Github <https://github.com/pommevilla/MetaFunPrimer/issues>`_.

Frequently Asked Questions
--------------------------

Q. I have <program> installed and I am able to call it on the command line, but when ``check_reqs.sh`` reports it as missing. :ref:`Answer <A1>`

.. _A1:

A. ``check_reqs.sh`` checks that the program is callable via the output of `hash <program>`. If you've created an alias for one of the programs, then the `hash` function will report that the program isn't callable. If you are certain that calling the program on the command line works, then you can continue running the variuos `mfp` programs. However, it is recommended for this pipeline to remove these aliases.  


Contact
-------

For any other issues or questions, email pev@iastate.edu.


