for f in roc_results/h3n2*; do
    res=$(tail -1 "$f")
    res2=${res//" "/","}
    res3=$(echo "$res2" | cut -f2- -d',')
    echo $res3
done
