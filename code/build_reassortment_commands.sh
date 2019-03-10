for i in {1..250}; do
	echo "python3 code/simulate_and_classify_reassortment_zoo.py -r $i > results/zoo_r_$i.out"
done

for i in {1..250}; do
	echo "python3 code/simulate_and_classify_reassortment_zoo.py -n $i > results/zoo_n_$i.out"
done

for i in {1..250}; do
	echo "python3 code/simulate_and_classify_reassortment_h3n2.py -r $i > results/h3n2_r_$i.out"
done

for i in {1..250}; do
	echo "python3 code/simulate_and_classify_reassortment_h3n2.py -n $i > results/h3n2_n_$i.out"
done
