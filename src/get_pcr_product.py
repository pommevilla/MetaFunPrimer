#!/usr/bin/python

# Takes a fasta file of primers and performs in silico PCR on an another file
# Usage: python modi_get_pcr_product.py test_primer1.fa test_target1.fa > degen_primer_1205_amoA_out.txt
# Input:
#   - test_primer1.fa: a fasta file of primer sequences
#   - test_target1.fa: a fasta file of potential target genes
# Output:
#   Prints out the following tab-separated columns to stdin:
#   - Sequence amplified
#   - Gene description
#   - The name of the forward primer
#	- The sequence of the forward primer
#   - The name of the reverse primer
#	- The sequence of the reverse primer
#	- The start position of the forward primer on the amplified sequence
#   - The start position of the reverse primer on the amplified sequence
#   - The length of the product
#
#	Recommend to run `awk '!_[$0]++' degen_primer_1205_amoA_out.txt` to remove the duplicate results and keep the single output lines

import sys
import re



def reverse_complement(nuc_sequence):
    """
    Returns the reverse complement of a nucleotide sequence.
    >>> reverse_complement('ACGT')
    'ACGT'
    >>> reverse_complement('ATCGTGCTGCTGTCGTCAAGAC')
    'GTCTTGACGACAGCAGCACGAT'
    >>> reverse_complement('TGCTAGCATCGAGTCGATCGATATATTTAGCATCAGCATT')
    'AATGCTGATGCTAAATATATCGATCGACTCGATGCTAGCA'
     """
    complements = {
    	"A": "T",
    	"C": "G",
    	"G": "C",
    	"T": "A"
    }
    rev_seq = "".join([complements[s] for s in nuc_sequence[::-1]])
    return rev_seq


def common_data(list1, list2): 
    result = False  
    for x in list1:   
        for y in list2: 
            if x == y: 
                result = True
                return result  
                  
    return result 


#fout = open("test_out.txt", "w")

def get_product(fpri, rpri, se, name):
    product = ''
    psize = 0
    pfpri = ''
    prpri = ''
    #fout = open("test_out.txt", "a")
    for x in fpri:  # x is the key of the dict fpri, x is the sequence
        ma = [m.start() for m in re.finditer(x, se)]        
        if len(ma) > 0:
            for st in ma:
                tempseq = se[st:]
                for y in rpri:
                    rma = [m.start() for m in re.finditer(y, tempseq)]
                    if len(rma) > 0:
                        # build an array based on x's forward primer cluster ID, [c001, c002, ...]
                        fpri_li = fpri[x].split(",")
                        for i, ff in enumerate(fpri_li):
                            f = ff.split(".")[-2]
                            fpri_li[i] = f
                            #print(fpri_li)
                                                
                        # build an array based on y's reverse primer cluster ID, [c001, c002, ...]
                        rpri_li = rpri[y].split(",")
                        for j, rr in enumerate(rpri_li):
                            r = rr.split(".")[-2]
                            rpri_li[j] = r
                        #print(rpri_li)
                        
                        for rst in rma:
                            # check if there're at least one pair of forward and reverse primers ID are from the same cluster
                            if common_data(fpri_li, rpri_li):   
                                product = tempseq[:rst+len(y)]
                                psize = len(product)
                                if (psize >= len(x) + len(y)):
                                    pfpri = x
                                    prpri = y
                                    prim_pair = fpri[pfpri] + "=" + rpri[prpri]
                                    sim_name = name.split()[0]
                                    des = name.split()[1:]
                                    if(len(des) > 0):
                                        descr = "_".join(des)
                                    else:
                                        descr = "_"
                                    print(">{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}".format(sim_name, descr, fpri[pfpri], pfpri, rpri[prpri], reverse_complement(prpri), prim_pair, st, st+ rst + len(y), psize))
                                
                                                        
                            
    #fout.write(">{}\t{}\t{}\t{}\t{}\t{}\n".format(sim_name, fpri[pfpri], rpri[prpri], st, st+ rst + len(y), psize))
#fout.close()


def find_product(fpri, rpri, file):
    with open(file, 'r') as seqs:
        name = ''
        flag = 0
        seq =[]
        for line in seqs:
            if(line[:1] == ">" and flag == 0):
                name = line.strip()[1:]
                flag = 1
            elif(line[:1] == ">" and flag == 1):
                se = ''.join(seq).upper()
                get_product(fpri,rpri,se,name)
                name = line.strip()[1:]
                seq = []
            else:
                seq.append(line.strip())
        se = ''.join(seq).upper()
        get_product(fpri, rpri, se, name)


        
def read_primer(file):
    with open(file, 'r') as prim:
        fpri = {}
        rpri = {}
        name = ""
        for line in prim:
            if(line[:1] == ">"):
                ptype = line.strip()[1]
                nameL = line.strip().split(".")
                name = ptype + "." + nameL[-2] + "." + nameL[-1]
            else:
                seq = line.strip()
                seq = seq.upper()
                rseq = reverse_complement(seq)
                if name[0] == 'F':
                    if seq in fpri:
                        temp = fpri[seq] + ',' + name
                        fpri[seq] = temp
                    else:
                        fpri[seq] = name
                if name[0] == 'R':
                    if seq in rpri:
                        temp = rpri[rseq] + ',' +name
                        rpri[rseq] = temp
                    else:
                        rpri[rseq] = name
        #print(fpri)
        #print(rpri)
    return fpri, rpri


            
def main():
	# Read primers from primers.fa
	#prim = open(sys.argv[1], 'r')
    prim = sys.argv[1]
    fpri, rpri = read_primer(prim)
    
	# Find products of primers from sequences.fa
    seqs = sys.argv[2]
    find_product(fpri, rpri, seqs)
    

if __name__ == '__main__':
	main()
