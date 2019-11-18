#!/usr/bin/python

# Converts the primer sequences from the output of EcoFunPrimer into fasta format
# Usage: python get_fasta_from_design.py input.rdp 
# Input:
#   - input.rdp: a file output from EcoFunPrimer
# Output:
#   - Prints out the sequences of input.rdp in fasta format to stdin
 
import sys

def main():
    num = 0
    file = sys.argv[1]
    for line in open(file,'r'):
        if line[:13] == "Primer Pair: " :
            prim = {}
            num += 1
            spl = line.strip().split("revOligo")
            for i in range(0, len(spl)):
                oli =  spl[i].split("seq=")
                snum = 0
                for j in range(1, len(oli)):
                    snum += 1
                    oneoli = oli[j].split("}")
                    cnu = str(num)
                    pnu = str(snum)
                    if len(cnu) == 1:
                        cnu = "00" + cnu
                    elif len(cnu) == 2:
                        cnu = "0" + cnu
                    
                    if len(pnu) == 1:
                        pnu = "0" + pnu

                    if(i == 0):
                        print( ">F:{}.C{}.{}F".format(file, cnu, pnu))
                        print(oneoli[0])
                    else:
                        print(">R:{}.C{}.{}R".format(file, cnu, pnu))
                        print(oneoli[0])


if __name__ == '__main__':
    main()
