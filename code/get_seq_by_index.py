""" Retrieves the nth sequence from a fasta """

if __name__ == "__main__":
	import sys
	from Bio import SeqIO
	c = 0
	fname = sys.argv[1]
	n = int(sys.argv[2])
	for i, r in enumerate(SeqIO.parse(fname, "fasta")):
		if i == n:
			print(">"+r.description)
			print(str(r.seq))
			sys.stderr.write("Fetching " + str(n) + r.description+"\n")

		
