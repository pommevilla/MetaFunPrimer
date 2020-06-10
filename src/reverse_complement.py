#!/usr/bin/python 

# import sys

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

# def main():
#     seq = sys.argv[1]
#     print(reverse_complement(seq))

if __name__ == "__main__":
    import doctest
    doctest.testmod()
