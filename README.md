# ArrowSAM

ArrowSAM is an in-memory Sequence Alignment/Map (SAM) representation which uses [Apache Arrow framework](https://arrow.apache.org/) (A cross-language development platform for in-memory data) and [Plasma (Shared-Memory) Object Store](https://arrow.apache.org/blog/2017/08/08/plasma-in-memory-object-store/) to store and process SAM columnar data in-memory. 

### <a name="cite"></a>Citing ArrowSAM

If you use ArrowSAM in your work, please cite:

> Ahmad et al., (2020). "ArrowSAM: In-Memory Genomics Data Processing Using Apache Arrow
> *Bioinformatics*, **34**:3094-3100. [doi:10.1093/bioinformatics/bty191](doi)

This repo contains following three components:

1. ArrowSAM (In-memory SAM data representation) integrated [BWA-MEM](https://github.com/tahashmi/bwa), Picard and GATK tools.<br />

2. A Singularity container def file (To create an environment to use all Apache Arrow related tools and libraries for ArrowSAM).<br />

3. Scripts to run different GATK best practices recommended workflows (using different in-memory data placement techniques like ArrowSAM, ramDisk and pipes for fast processing) to run complete DNA analysis pipeline efficiently.<br />

Note: ArrowSAM and all other workflows are based on single node, multi-core machines.

## How to run 
1. Install [Singularity](https://sylabs.io/docs/) container
2. Download our Singularity [script](https://github.com/abs-tudelft/arrow-gen/tree/master/Singularity) and generate singularity image (this image contains all Arrow related packges necessary for building/compiling BWA-MEM, Picard and GATK)
3. Now enter into generated image using command:
         
        sudo singularity shell <image_name>.simg
4. Download [BWA-MEM](https://github.com/tahashmi/bwa) inside image
       
        git clone https://github.com/tahashmi/bwa.git
5. Go into bwa dir and compile BWA-MEM:

        cd bwa
        make
6. Now you can run BWA-MEM. 
