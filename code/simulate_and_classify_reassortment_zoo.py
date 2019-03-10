import subprocess as sp
import sys
from Bio import SeqIO
import random
from Bio import pairwise2
from simulate_seqs import *

def levenshtein(s1, s2):
	aln = pairwise2.align.globalms(s1, s2, 0,-1,-1,-1, one_alignment_only=True, score_only=True)
	return aln

# First generate the genome segments, takes the first argument, -r, or -n for reassort and no reassort
genome_segments = [[k for k in l.split("\n") if k != ''] for l in sp.check_output("python3 code/generate_reassorted_genome_zoo.py %s" % sys.argv[1], shell=True).decode("utf-8").split(">") if l != '']
reads = []
true_names = ""
for gs in genome_segments:
	name = gs[0]
	ref = gs[1]
	true_names += name+","
	reads += readize_random([ref], N=1000)
true_names = true_names[:-1]

# Take a random tag $i$
# Write the reads
i = sys.argv[2]
readstr = ""
tmpfq = "tmp/tmp"+str(i)+".fq"
sp.call("cat /dev/null > %s" %tmpfq, shell=True)
random.shuffle(reads)
write_reads(reads, "unknown", tmpfq)

# Lastly, call the reads with VAPOR
segs = "HA MP NA NP NS PA PB1 PB2".split(" ")
seg_refsnames = ["res/A_allsp_genomes_nf_%s.fa" % l for l in segs]
vapornames = ""
for seg_refn in seg_refsnames:
    # VAPOR
    vapor_out = [l for l in sp.check_output("vapor.py -fa %s -fq %s" % (seg_refn, tmpfq), shell=True).decode("utf-8").split("\n") if l != ''][0]

    # OUTPUT
    vp_choice_name =  " ".join(vapor_out.split()[4:])
    sys.stderr.write(vapor_out+"\n")
    sys.stderr.write(vp_choice_name+"\n")
    vapornames += vp_choice_name + ","

vapornames = vapornames[:-1]
print(true_names,"#",vapornames)
