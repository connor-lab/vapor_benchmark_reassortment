from Bio import SeqIO
from itertools import groupby
import random
import sys

hgfname = "res/A_human_genomes_nf.fa"
agfname = "res/A_avian_genomes_nf.fa"
sgfname = "res/A_swine_genomes_nf.fa"
def get_genomed(fname):
    genomed = {}
    for r in SeqIO.parse(fname, "fasta"):
        spl = r.description.split()
        strain = " ".join(spl[1:-2])
        if strain not in genomed:
            genomed[strain] = [r]
        else:
            genomed[strain].append(r)
    todel = []
    for i,q in genomed.items():
        if len(q) != 8:
            todel.append(i)
    for t in todel:
        del genomed[t] 
    # finally sort
    for i,q in genomed.items():
        genomed[i] = sorted(genomed[i], key=lambda x:x.description.split()[-1])
    return genomed

hgd = get_genomed(hgfname) 
agd = get_genomed(agfname)
sgd = get_genomed(sgfname)
zgd = agd.copy()
zgd.update(sgd) 

# Generate 500 non-reassortments and 500 reassortments, interleaved
# Demarcated by a ***
if sys.argv[1] != "-r":
	g1,g1r = random.choice(list(hgd.items()))
	for r in g1r:
		print(">"+r.description)
		print(str(r.seq))
else:
	g2,g2r = random.choice(list(hgd.items()))
	z2,z2r = random.choice(list(zgd.items()))
	roll = random.randint(0,7)
	for ri in range(len(g2r)):
		if ri == roll:
		    r = z2r[ri]
		else:
		    r = g2r[ri]
		print(">"+r.description)
		print(str(r.seq))


	    
    

