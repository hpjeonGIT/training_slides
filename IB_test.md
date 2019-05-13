# Intel MPI
- Select fabrics
    - cat /etc/dat.conf
    - export I_MPI_FABRICS=shm:dapl
- I_MPI_ADJUST
    - https://software.intel.com/en-us/articles/intel-mpi-library-collective-optimization-on-intel-xeon-phi
    - https://software.intel.com/en-us/mpi-developer-reference-windows-i-mpi-adjust-family
    - export I_MPI_ADJUST_ALLTOALL=1
- In mpirun command, use `-genv I_MPI_DEBUG 5` to print debug information

# OpenMPI
- ompi_info --display-map to display information of the current openmpi

# IB command
- ibstat

# Nvidia Peer Memory
- In order to check nv_peer_mem is loaded:
    - $ service nv_peer_mem status
    - nv_peer_mem module is loaded.
- Testing CUDA latency
    - REf: http://www.mellanox.com/related-docs/prod_software/Mellanox_GPUDirect_User_Manual_v1.0.pdf

# Status of IB and RDMA
- Ref: http://www.rdmamojo.com/2015/01/24/verify-rdma-working/
- command
    - ibv_devices
    - lsmod |grep rdm
    - ibv_devinfo -d mlx5_0
- Test
    - hostA: ib_send_bw -d mlx5_0 -i 1 -F --report_gbits
    - hostB:  ib_send_bw -d mlx5_0 -i 1 -F --report_gbits
- Open Fabric info
    - ofed_info

# NCCL test
- Hangs in CENTOS7.3
- Requirement for glibc >=2.19 but runs in CentOS7.4 which has 2.17
    - Check: https://github.com/NVIDIA/nccl/issues/19#issuecomment-213223260
    - https://github.com/NVIDIA/nccl/issues/19#issuecomment-213223260
    - pci setup might be necessary
```    
sudo lspci | grep PLX
sudo lspci -vvv | grep ACSCtl

sudo setpci -s 03:00.0 f2a.w=0000
sudo setpci -s 04:08.0 f2a.w=0000
```
- https://github.com/NVIDIA/nccl-tests
    - Setup NCC_HOME, MPI_HOME and build using make
    - ./build/all_reduce_perf -b 8 -e 128M -f 2 -g 4
    - mpirun -n 1 ./build/all_reduce_perf -b 8 -e 128M -f 2 -g 4 
        - This uses 4 gpus per node

# find ip address
- ifconfig is deprecated. Use `ip a`
- IB's ip is different than ethernet ip
