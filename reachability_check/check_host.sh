
awk '{print $1}' $1 | while read line
do
        nc -v -z -w 3 $line $2 &> /dev/null && echo "$line: Online" || echo "$line: Offline"
done
