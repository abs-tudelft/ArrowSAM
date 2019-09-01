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
  

def run_md(lines):
    """MD."""
    # Get the dataframe from the object store.
    #print(object_id)
    Chr = lines[0]
    Chr_header = Chr.split('_')[0]
    lines = lines[1]
    p = subprocess.Popen(["java", "-Djava.library.path=/usr/local/lib/", "-jar", "/home/tahmad/bulk/apps/picard/picard.jar", "MarkDuplicates", "I=/home/tahmad/bulk/apps/picard/headers/header_"+''.join(Chr_header)+''.join(".bam"), "O=/home/tahmad/bulk/apps/picard/marked_duplicates.bam", "M=/home/tahmad/bulk/apps/picard/marked_dup_metrics.txt", "Chr="+''.join(Chr), "Plasma="+''.join(lines)], stdout=subprocess.PIPE)
    
    p.communicate()
    return 0, 0

if __name__ == '__main__':
    parallel_md_start = time.time()
    #os.remove('/home/tahmad/bulk/apps/bwa/objIDsJava.txt')
  
    lines = [line.split('\t') for line in open('/home/tahmad/bulk/apps/objIDsPy.txt')]
    #print(lines)
    #lines = lines[:1]

    if os.path.exists("/home/tahmad/bulk/apps/objIDsJavaFlag.txt"):
        os.remove("/home/tahmad/bulk/apps/objIDsJavaFlag.txt")

    #print(lines)
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


