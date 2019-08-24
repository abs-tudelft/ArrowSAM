BootStrap: debootstrap
OSVersion: bionic
MirrorURL: http://us.archive.ubuntu.com/ubuntu/


%runscript
    #!/bin/sh
    #exec "$@"
    echo "Starting run script..."
    #chmod 777 /root/apps/test.sh
    #run_all_hpc.sh
    /home/tahmad/bulk/apps/test.sh 
    /home/tahmad/bulk/apps/run_all.sh 

%files
    # Copy tools from /root/tools to /tools
    #/root/tools / 

%post
    echo "Hello from inside the container"
    sed -i 's/$/ universe/' /etc/apt/sources.list
    apt-get -y update
    apt-get -y upgrade
    apt-get -y dist-upgrade
    apt-get -y install vim
    apt-get install -y curl
    apt-get install cmake -y
    pip install ray
    pip install psutil
    apt-get install -y software-properties-common
    #apt-get install add-apt-repository
    add-apt-repository ppa:chris-lea/redis-server
    apt-get update
    apt-get install redis-server -y
    apt-get install openmpi-bin -y
    apt-get update && apt-get install -y python3
    apt-get update && apt install -y python-pip
    apt-get update && pip install pyarrow
    apt-get update && pip install pandas
    apt-get update && apt install -y maven
    apt-get update && apt-get install -y openjdk-8-jre
    apt-get update && apt-get install -y openjdk-8-jdk
    apt-get update && apt-get install -y gtk-doc-tools
    apt-get update && apt-get install -y libglib2.0-dev
    apt-get update && apt-get install -y libtool-bin
    apt-get update && apt-get install -y autoconf
    apt-get update && apt-get install -y libgirepository1.0-dev
    apt-get update && apt-get install -y sshfs
    apt-get update && apt-get install sysstat -y
    apt-get update && apt-get install dstat
    apt-get update && apt install -y git
    apt-get update && apt-get install -y linux-tools-generic
    apt-get clean

    # Create mount points for network drives
    # mkdir -p /shares/{bulk,group}

    #mv /usr/lib/x86_64-linux-gnu/openmpi/lib/libmpi.so.20.10.1 /usr/lib/x86_64-linux-gnu/openmpi/lib/libmpi.so.12


%environment
    export PATH=$PATH:/usr/local/bin
    JAVA_HOME=/usr/bin/java
    export TOOLS_PREFIX='/usr/local'
    export GCC_VERSION='5.5.0'
    export BOOST_VERSION='1_67_0'
    export CPATH='/usr/local/include:/usr/lib'
    export PKG_CONFIG_PATH='/usr/local/lib/pkgconfig'
    export LD_LIBRARY_PATH='/usr/lib:/usr/lib/x86_64-linux-gnu:/usr/local/lib:/usr/lib/x86_64-linux-gnu/openmpi/lib'
    export PATH=$TOOLS_PREFIX/bin:$PATH
    echo $LD_LIBRARY_PATH


