import sys
from Bio import SeqIO
from Bio import pairwise2

# Firstly, get a dictionary of HA sequences
HAd = {}
for r in SeqIO.parse(sys.argv[1], "fasta"):
    strain = " ".join(r.description.split()[1:-2])
    if strain not in HAd:
        HAd[strain] = str(r.seq)

# Now do the classification
sys.stderr.write("THE FOLLOWING PARAMETERS MUST BE CORRECT: param, true_positive_fname, true_negative_fname. FAILURE TO PROVIDE TRUE_POSITIVE_FNAME AND TRUE_NEGATIVE_FNAME IN THE CORRECT ORDER WILL RESULT IN INVERTED RESULT\n")
TP = 0
TN = 0
FP = 0
FN = 0
param = float(sys.argv[2])
true_positive_fname, true_negative_fname = sys.argv[3:5]
with open(true_positive_fname) as f:
    true_positive_lines = [l for l in f]

with open(true_negative_fname) as f:
    true_negative_lines = [l for l in f]

# Interleave and flatten
interleaved = [x for t in zip(true_positive_lines, true_negative_lines) for x in t]

for li, line in enumerate(interleaved):
    print(line.split("#"))
    calls = line.split("# ")[1]
    segment_classifications = calls.split(",")
    strains = []
    for ri, segment in enumerate(segment_classifications):
        strain = " ".join(segment.split()[2:-2])
        strains.append(strain)
        
    scores = []
    done_combos = set()
    for strain in strains:
        # For each one, perform global alignment with the other strains
        # for each strain that was classified for this genome, take pairwise distasnce to the segment chosen
        seg1 = HAd[strain]
        for strain2 in strains:
            if strain != strain2 and (strain, strain2) not in done_combos and (strain2, strain) not in done_combos:
                seg2 = HAd[strain2]
                aln = -1*pairwise2.align.globalms(seg1, seg2, 0, -1, -1, -1, score_only=True, one_alignment_only=True)
                scores.append(100*(1.0-aln/len(seg1)))
                done_combos.add((strain,strain2))
                done_combos.add((strain2,strain))
    if len(set(strains)) == 1:
        scores = [100.]
    mini = min(scores)
    print(mini)
    if li % 2 == 0:
        # positive number
        if mini < param:
            print("True positive", mini)
            TP += 1
        else:
            print("False positive", mini)
            FN += 1
    else:
        if mini < param:
            print("False negative", mini)
            FP += 1
        else:
            print("True negative", mini)
            TN += 1
    print()
    
total = TP + FN + FP + TN
TPR = TP/(TP+FN)
FPR = FP/(TN+FP)
print("RESULT: %f %f %f" %(param,TPR,FPR))
            


