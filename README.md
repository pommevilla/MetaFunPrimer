# MetaFunPrimer

[![Build Status](https://travis-ci.com/pommevilla/MetaFunPrimer.svg?branch=master)](https://travis-ci.com/pommevilla/MetaFunPrimer)

A pipeline to design high-throughput qPCR primers to target environmentally abundant genes. See [the documentation](https://metafunprimer.readthedocs.io/) for installation instructions and a demonstration of the pipeline.

*Latest version: v0.90.4, 3/2/2020*

## Programs required

*The versions listed after each program are those used in the testing of the pipeline.*  

* CD-HIT (v4.6.8)
* Diamond (v0.9.14)
* Clustal Omega (v1.2.4)
* BLAST (v2.7.1+)
* EcoFunPrimer
* Parallel

## Instructions

MetaFunPrimer requires the following input files:

* Nucleotide and protein sequences of the genes of interest
* Metagenome files for your environment of interest
