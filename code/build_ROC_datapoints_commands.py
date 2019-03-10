import subprocess as sp
import numpy as np

for i in np.linspace(90,99,41):
	com = "python3 code/get_ROC_datapoint.py res/HA_A_avhusw_nf.fa %f zoo_r.out zoo_n.out > roc_results/zoo_roc_%f.out" % (i,i)
	print(com)

for i in np.linspace(90,99,41):
	com = "python3 code/get_ROC_datapoint.py res/A_H3N2_human_genomes_nf_HA.fa %f h3n2_r.out h3n2_n.out > roc_results/h3n2_roc_%f.out" % (i,i)
	print(com)


