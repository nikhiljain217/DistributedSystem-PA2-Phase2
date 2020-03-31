i=$1
j=0
while [ $j -le $i ]
do
python3 server.py 1000$j $i &
j=`expr $j + 1`
done
