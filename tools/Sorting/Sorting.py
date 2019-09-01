from multiprocessing import Pool
import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.plasma as plasma
import subprocess
import time
import random
import string
import multimerge
import os
import os.path

client = None

# Connect to clients
def connect():
    global client
    client = plasma.connect('/tmp/store0', "", 0)

def local_sort(object_id):
    """Sort a partition of a dataframe."""
    # Get the dataframe from the object store.
    #print(object_id)
    [df] = get_dfs_arrow([object_id])#get_dfs([object_id])
    # Sort the dataframe.
    sorted_df = df.sort_values(by='beginPoss')
    client.delete([object_id])
    return put_df(sorted_df)#, 0#put_df(sorted_df), 1#sorted_df.as_matrix().take(indices)

def get_dfs_arrow(object_ids):
    buffers = client.get_buffers(object_ids)
    return [pa.read_record_batch(pa.BufferReader(buf), test_schema()).to_pandas() for buf in buffers]

def test_schema():
    fields = [
        pa.field('qNames', pa.string()),
	pa.field('flags', pa.int32()),
	pa.field('rIDs', pa.int32()),
	pa.field('beginPoss', pa.int32()),
	pa.field('mapQs', pa.int32()),

	pa.field('cigars', pa.string()),

	pa.field('rNextIds', pa.int32()),
	pa.field('pNexts', pa.int32()),
	pa.field('tLens', pa.int32()),

        pa.field('seqs', pa.string()),
        pa.field('quals', pa.string()), #issue TODO
        pa.field('tagss', pa.string())

    ]
    return pa.schema(fields)

def put_df(df):
    id_num = df['rIDs'].values[0]
    id_num = str(id_num)
    if id_num == '23':
	id_num = 'X'
    elif id_num == '24':
	id_num = 'Y'
    elif id_num == '25':
	id_num = 'M'
	
    record_batch = pa.RecordBatch.from_pandas(df)
    record_batch_rows = record_batch.num_rows
    record_batch_rows_actual = record_batch_rows
    index = 0
    limit = 5714285
    check = False
    print(record_batch_rows_actual)
    i = 0
    while record_batch_rows > limit:

        check = True
        record_batch_rows = record_batch_rows -limit
        record_batch_slice = record_batch.slice(index, limit)
        index = index + limit 
        
        
 	# Get size of record batch and schema
        mock_sink = pa.MockOutputStream()
        stream_writer = pa.RecordBatchStreamWriter(mock_sink, record_batch_slice.schema)
        stream_writer.write_batch(record_batch_slice)
        data_size = mock_sink.size()
    
        # Generate an ID and allocate a buffer in the object store for the
        # serialized DataFrame
        object_id = plasma.ObjectID(''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20)))
        #print(id_num)
        buf = client.create(object_id, data_size)

        # Write the serialized DataFrame to the object store
        sink = pa.FixedSizeBufferWriter(buf)
        stream_writer = pa.RecordBatchStreamWriter(sink, record_batch_slice.schema)
        stream_writer.write_batch(record_batch_slice)

        # Seal the object
        client.seal(object_id)

        f = open("/home/tahmad/bulk/apps/objIDsPy.txt","a")
        f.write('Chr'+id_num+'_'+str(i)+'\t'+object_id.binary() + '\n') 
        f.close()
        i = i+1

    if check == True: 
        record_batch = record_batch.slice(index, record_batch_rows)


    # Get size of record batch and schema
    mock_sink = pa.MockOutputStream()
    stream_writer = pa.RecordBatchStreamWriter(mock_sink, record_batch.schema)
    stream_writer.write_batch(record_batch)
    data_size = mock_sink.size()
    
    # Generate an ID and allocate a buffer in the object store for the
    # serialized DataFrame
    object_id = plasma.ObjectID(''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20)))
    #print(id_num)
    buf = client.create(object_id, data_size)

    # Write the serialized DataFrame to the object store
    sink = pa.FixedSizeBufferWriter(buf)
    stream_writer = pa.RecordBatchStreamWriter(sink, record_batch.schema)
    stream_writer.write_batch(record_batch)

    # Seal the object
    client.seal(object_id)

    #get_df(object_id) #Loopback

    return object_id, id_num

if __name__ == '__main__':
    print("Hello")
    parallel_sort_start = time.time()
    
    lines = [line.split('\t')[1][:20] for line in open('/home/tahmad/bulk/apps/objID.txt')]
    #print(lines)
    lines = lines[:25]
    object_ids = [plasma.ObjectID(byte) for byte in lines]
    object_ids = object_ids[:len(lines)]
    #print(lines)

    # Connect to the plasma store.
    connect()

    if os.path.exists("/home/tahmad/bulk/apps/objIDsPy.txt"):
        os.remove("/home/tahmad/bulk/apps/objIDsPy.txt")

    # Connect the processes in the pool.
    pool = Pool(initializer=connect, initargs=(), processes=len(lines))
    #print(object_ids)
    [sorted_df_ids, id_nums] = list(zip(*pool.map(local_sort, object_ids)))
    #object_ids_back = [idnew for idnew in sorted_df_ids[0]]
    print(sorted_df_ids)
    print(id_nums)
    
    f = open("/home/tahmad/bulk/apps/objIDsPy.txt","a")
    [f.write('Chr'+id_num+'\t'+obj_id.binary() + '\n') for obj_id, id_num in zip(sorted_df_ids[:len(lines)], id_nums[:len(lines)])] 
    f.close()

    parallel_sort_end = time.time()

    print('Parallel sort took {} seconds.'
          .format(parallel_sort_end - parallel_sort_start))

