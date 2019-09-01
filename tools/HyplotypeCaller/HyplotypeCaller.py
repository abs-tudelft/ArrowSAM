# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
from multiprocessing import Pool
import subprocess
import time
import random
import string
import os

chrs_ids = ['Chr1','Chr2','Chr3','Chr4','Chr5','Chr6','Chr7','Chr8','Chr9','Chr10','Chr11','Chr12','Chr13','Chr14','Chr15','Chr16','Chr17','Chr18','Chr19','Chr20','Chr21','Chr22','ChrX','ChrY','ChrM']

def run_md(lines):
    """MD."""
    # Get the dataframe from the object store.
    Chr = lines[0]
    plasmaid = lines[1][:20]
    flag = lines[2]
    qual = lines[3]
    p = subprocess.Popen(["java", "-Djava.library.path=/usr/local/lib/", "-jar", "/home/tahmad/bulk/apps/gatk/gatk.jar", "HaplotypeCaller", "-R", "/dev/shm/tahmad/hg19/hg19.fasta", "-I", "/home/tahmad/bulk/apps/picard/headers/header_"+''.join(Chr)+''.join(".bam"), "-O", "/home/tahmad/bulk/apps/bsqr/"+''.join(Chr)+''.join(".vcf"), "-L","/home/tahmad/bulk/apps/bsqr/beds/"+''.join(Chr)+''.join(".bed"), "-ip","100", "Chr="+''.join(Chr), "Plasma="+''.join(plasmaid), "Flag="+''.join(flag), "Qual="+''.join(qual)], stdout=subprocess.PIPE)
    
    p.communicate()
    return 0, 0

if __name__ == '__main__':
    parallel_md_start = time.time()
    #os.remove('/home/tahmad/bulk/apps/bwa/objIDsJava.txt')
  
    lines = [line.split('\t') for line in open('/home/tahmad/bulk/apps/objIDsPy.txt')]

    ids = [line.split('\t')[1][:20] for line in open('/home/tahmad/bulk/apps/objIDsJavaFlag.txt')]
    chrs = [line.split('\t')[0] for line in open('/home/tahmad/bulk/apps/objIDsJavaFlag.txt')]
    flags = [ids[chrs.index(chrs_ids[i])] for i in range(len(chrs_ids))]    
    [lines[i].append(flags[i]) for i in range(len(chrs_ids))]

    ids = [line.split('\t')[1][:20] for line in open('/home/tahmad/bulk/apps/objIDsJavaQual.txt')]
    chrs = [line.split('\t')[0] for line in open('/home/tahmad/bulk/apps/objIDsJavaQual.txt')]
    quals = [ids[chrs.index(chrs_ids[i])] for i in range(len(chrs_ids)-1)]    
    [lines[i].append(quals[i]) for i in range(len(chrs_ids)-1)]

    lines = lines[:24]

    #object_ids = [plasma.ObjectID(byte) for byte in lines]
    #object_ids = object_ids[:len(lines)]
    #print(object_ids)

    # Connect the processes in the pool.
    pool = Pool(initargs=(), processes=len(lines))

    # Begin timing the parallel Mark Duplicate.
    #parallel_md_start = time.time()

    sorted_df_ids = list(zip(*pool.map(run_md, lines)))

    parallel_md_end = time.time()

    print('Parallel md took {} seconds.'
          .format(parallel_md_end - parallel_md_start))


