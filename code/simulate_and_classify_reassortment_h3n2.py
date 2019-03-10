import subprocess as sp
import sys
from Bio import SeqIO
import random
from Bio import pairwise2
from simulate_seqs import *
import random

def levenshtein(s1, s2):
	aln = pairwise2.align.globalms(s1, s2, 0,-1,-1,-1, one_alignment_only=True, score_only=True)
	return aln

# Generate reads from each genome segment, uniformly, takes arguments -n, or -r for no reassortment and reassortment
genome_segments = [[k for k in l.split("\n") if k != ''] for l in sp.check_output("python3 code/generate_reassorted_genome_h3n2.py %s" % sys.argv[1], shell=True).decode("utf-8").split(">") if l != '']
reads = []
true_names = ""
for gs in genome_segments:
	name = gs[0]
	ref = gs[1]
	true_names += name+","
	reads += readize_random([ref], N=1000)
true_names = true_names[:-1]

# Write the reads
i = sys.argv[2]
readstr = ""
tmpfq = "tmp/tmp"+str(i)+".fq"
sp.call("cat /dev/null > %s" %tmpfq, shell=True)
random.shuffle(reads)
write_reads(reads, "unknown", tmpfq)

# Next classify each of the segments with VAPOR
segs = "HA MP NA NP NS PA PB1 PB2".split(" ")
seg_refsnames = ["res/A_H3N2_human_genomes_nf_%s.fa" % l for l in segs]
vapornames = ""
for seg_refn in seg_refsnames:
    # Call VAPOR
    vapor_out = [l for l in sp.check_output("vapor.py -fa %s -fq %s" % (seg_refn, tmpfq), shell=True).decode("utf-8").split("\n") if l != ''][0]

    # Get OUTPUT
    vp_choice_name =  " ".join(vapor_out.split()[4:])
    vapornames += vp_choice_name + ","

# Output segment calls
vapornames = vapornames[:-1]
print(true_names,"#",vapornames)
