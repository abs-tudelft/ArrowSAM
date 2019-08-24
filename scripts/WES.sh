
echo -----------BWA-MEM-------------- 
echo BWA-MEM started; date
plasma_store_server -m 25000000000 -s /tmp/store0 & ~/bulk/apps/bwa/bwa mem -t 25 /dev/shm/tahmad/hg19/hg19.fasta /dev/shm/tahmad/gcat_025/gcat_025_1.fastq /dev/shm/tahmad/gcat_025/gcat_025_2.fastq
echo bwa mem done; date

echo -----------Plasma-Sorting-------------- 
echo started; date

python ~/bulk/apps/sorting/sort_processes.py 
echo plasma sorting done; date

echo -----------Plasma-MD-------------- 
echo started; date
python ~/bulk/apps/sorting/md_processes.py 
echo plasma md done; date

#Working

echo -----------Plasma-BSQR-------------- 
echo started; date
python ~/bulk/apps/bsqr/bsqr_processes.py 
echo plasma bsqr done; date

echo -----------Plasma-ApplyBSQR-------------- 
echo started; date
python ~/bulk/apps/bsqr/apply_bsqr_processes.py 
echo plasma appply_bsqr done; date

echo -----------Plasma-Hyplo-------------- 
echo started; date
python ~/bulk/apps/bsqr/hyplo_processes.py 
echo plasma hyplo done; date


#echo -----------Killing Plasma!-------------- 
kill $(pidof plasma_store_server)
