for f in roc_results/zoo*; do
    res=$(tail -1 "$f")
    res2=${res//" "/","}
    res3=$(echo "$res2" | cut -f2- -d',')
    echo $res3
done
