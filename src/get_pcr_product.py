#!/usr/bin/python

# Takes a fasta file of primers and performs in silico PCR on an another file
# Usage: get_pcr_product.py primers.fa sequences.fa
# Input:
#   - primers.fa: a fasta file of primer sequences
#   - sequences.fa: a fasta file
# Output:
#   Prints out the following tab-separated columns to stdin:
#       - Sequence amplified
#       - The name of the forward primer
#       - The start position of the forward primer on the amplified sequence
#       - The name of the reverse primer
#       - The start position of the reverse primer on the amplified sequence
#       - The length of the product
#       - The amplified sequence    

import sys
import reverse_complement
import re

def get_product(fpri,rpri,se,name):
    print "target\tforward\tproduct_start\treverse\tproduct_end\tlength\tproduct"
    product = ''
    psize = 0
    pfpri = ''
    prpri = ''
    for x in fpri.items():
        ma = [m.start() for m in re.finditer(x[0], se)]
        if len(ma) > 0:
            for st in ma:
                tempseq = se[st:]
                for y in rpri.items():
                    rma = [m.start() for m in re.finditer(y[0],tempseq)]
                    if len(rma) > 0 :
                        for rst in rma:
                            product = tempseq[:rst+len(y[0])]
                            psize = len(product)
                            pfpri = x[0]
                            prpri = y[0]
                            print ">%s\t(%s)\t%s\t(%s)\t%s\t%s\t%s" %(name, fpri[pfpri], st, rpri[prpri], st+rst+len(y[0]),len(product), product)
    return 0

def find_product(fpri,rpri,seqs):
    name = ''
    flag = 0
    seq =[]
    for line in seqs:
        if(line[:1] == ">" and flag == 0):
            name = line.strip()[1:]
            flag = 1
        elif(line[:1] == ">" and flag == 1):
            se = ''.join(seq)
            get_product(fpri,rpri,se,name)
            name = line.strip()[1:]
            seq = []
        else:
            seq.append(line.strip())
    se = ''.join(seq)
    get_product(fpri,rpri,se,name)
        
def read_primer(prim):
    swi = 0
    fpri = {}
    rpri = {}
    name = ""
    for line in prim:
        if(line[:1] == ">"):
            name = line.strip()[1:]
        else:
            seq = line.strip()
            rseq = reverse_complement.reverse_complement(seq)
            if fpri.has_key(seq):
                temp = fpri[seq] + ','+name
                fpri[seq] = temp
                temp = rpri[rseq] + ',' +name
                rpri[rseq] = temp
            else:
                fpri[seq] = name
                rpri[rseq] = name

    return fpri,rpri
            
def main():
    #read primer
    prim = open(sys.argv[1],'r')
    seqs = open(sys.argv[2],'r')
    fpri,rpri = read_primer(prim)

    #find product
    find_product(fpri,rpri,seqs)

if __name__ == '__main__':
    main()
