#!/usr/bin/python
# -*- coding: utf-8 -*-

# Take the output file from get_pcr_product.py, filter out the most efficient and specific final primer pairs,
# extract and format the output file of MetaFunPrimer 
# Usage: python filter_primers_output.py pcr_output.txt

# Input: pcr_output.txt
# Output: final_output_primer.txt

"""
Created on Sat Mar 14 18:00:07 2020
@author: liujia
"""

import sys
import copy

# a helper function for get_prim function
def get_max_prim(dic):
    max = 0
    prim = ""
    for i in dic:
        gn = dic[i]
        gnl = gn.split()
        count = len(gnl)        
        if max < count:
            max = count
            prim = i
    return prim

# Read in-silico pcr output and get one list of genes that can be targeted and 
# one dictionary with primers as key and genes it can target as values 
def read_file(file):
    with open(file, 'r') as ori_f:
        pair_dic = {}
        genes = []
        for line in ori_f:
            li = line.strip().split()
            gs = li[0] + "_" + li[1]
            gs = "_".join(gs.split()) # make sure no space
            if gs not in genes:
                genes.append(gs)
            # genes.append(gs)
            prim = li[-4]
            #print(prim)
            if prim in pair_dic:
                temp = pair_dic[prim] + ' ' + gs
                pair_dic[prim] = temp
            else:
                pair_dic[prim] = gs
    with open("mfpqpcr.log", 'w') as fout:
        for item in genes:
            fout.write("%s\n" % item[1:])
          
    return genes, pair_dic
    


# get the most efficient final primer list
def get_prim(pair_dic, genes):
    f_prim = []
    while genes:
        max_prim = get_max_prim(pair_dic)
        prim_genes = pair_dic[max_prim].split()
        
        # get the number of genes from 'genes' list been targeted by max_prim 
        # and add to final primer list if the number is bigger than 0;
        # update the genes list (by removing the genes that targeted by max_prim from genes list)
        num_tar = 0
        for g in prim_genes:
            if g in genes:
                genes.remove(g)
                num_tar += 1
        if num_tar > 0:
            f_prim.append(max_prim)
            
                
        # update the target genes of each primer in pair_dic 
        # (by removing the genes that being targeted by max_prim within each primer targeting genes list)
        for prim_key in pair_dic:
            gene_ele = pair_dic[prim_key].split()
            gene_ele = [gs for gs in gene_ele if gs not in prim_genes]
            temp = ' '.join(gene_ele)
            pair_dic[prim_key] = temp
        
        
    return f_prim
        
        
        
        
seps = "-" * 20


def main():
    # Read in file
    file = sys.argv[1]
    genes, pair_dic = read_file(file)
    
    # need to make a deep copy of pair_dic for extracting target genes for output
    pair_dic2 = copy.deepcopy(pair_dic)
   
    
    # Get the most efficient final primer pair list 
    final_prim = get_prim(pair_dic, genes)
    
    # extract and generate final output
    with open(file, 'r') as f:
        for line in f:
            line = line.split()
            pair = line[-4]
            if final_prim:
                if pair in final_prim:
                    tar_g = pair_dic2[pair]
                    tar_g = tar_g.replace(" ", "\n")
                    print("{}\t{}\t{}\t{}\t{}\n{}\n{}\n{}".format(line[2], line[3], line[4], line[5], line[-1], seps, tar_g, seps))
                    final_prim.remove(pair)
        #print(len(final_prim))

if __name__ == '__main__':
	main()

