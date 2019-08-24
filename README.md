# Arrow-Gen

ArrowSAM is an in-memory Sequence Alignment/Map (SAM) representation which uses Apache Arrow framework (A cross-language development platform for in-memory data) and [Plasma (Shared-Memory) Object Store](https://arrow.apache.org/blog/2017/08/08/plasma-in-memory-object-store/) to store and process SAM columnar data in-memory. 

This repo contains following three components:

1. ArrowSAM (In-memory SAM data representation) integrated BWA-MEM, Picard and GATK tools.<br />

2. A Singularity container def file (To create an environment to use all Apache Arrow related tools and libraries for ArrowSAM).<br />

3. Scripts to run different GATK best practices recommended workflows (using different in-memory data placement techniques like ArrowSAM, ramDisk and pipes for fast processing) to run complete DNA analysis pipeline efficeintly.<br />

Note: ArrowSAM and all other workflows are based on single node, multi-core machines.
