# Parallel programming environments in 90's
 - Ref: http://parlang.pbworks.com/f/programmability.pdf
 
# Introduction to MPI
- P2P
  - source -> target
  - Traditional message passing
  - MPI_Send, MPI_Isend, MPI_Recv, MPI_Irecv, ...
- One side communiction
  - RDMA (or RMA)
  - CPU offloading
  - Can be faster than message passing
- Collective
  - Per communicator
  - MPI_gather, MPI_allgather, MPI_reduce, MPI_allreduce, MPI_alltoall, ...
  - Highly importance in ML
- Offloading
  - NCCL

# MPI Tracing
- Why?
  - Profiling and characterizing communication pattern
  - This is NOT debugging
  - Essential for load-balancing
  - Figure out the the size/pair/frequency of MPI communication
- What tools?
  - mpiP: open-source, https://computing.llnl.gov/?set=code&page=mpip_llnl
  - mpitrace: IBM internal
  - Intel MPI tool: within intel MPI
  - Intel Trace Analyzer and Collector: ITAC, providing GUI
  - Allinea MAP provides similar profiling results
- Tracing overhead
  - Comprehensive tracing might affect performance
  - Check/compare wall time of bare run
  - Difference of wall time < 5% would be ideal

# Strategy of tracing
- Default
  - Use as it is
  - Trace all the code
- Define FOM
  - Assign Feature of Merit or Domain Of Interest
  - Ref: https://software.intel.com/en-us/node/535539
  - Trace will be done between MPI_Pcontrol

```C
MPI_Pcontrol(1, "DOI");
// Do something using MPI functions
MPI_Pcontrol(-1, "DOI");
```
# Practice
- module load intel
- source /share/compiler/intel/18.0/impi/2018.0.128/bin64/mpivars.sh
- make
- export OMP_NUM_THREADS=1
- export I_MPI_STATS=all
- mpirun -n 8 mpi_hello_world
- This produces stats.txt and stats.ipm
  - stats.ipm: Summary of MPI statistics
  - stats.txt: Communication statistics of each MPI rank
    - Pair wise or collective
    - Message size, frequency, time, ...
    
* ITAC
- Intel Trace Analyzer and Collector
- https://software.intel.com/en-us/node/535592
- module load intel
- source /share/compiler/intel/18.0/impi/2018.0.128/bin64/mpivars.sh
- source /share/compiler/intel/18.0/itac/2018.0.015/bin/itacvars.sh 
- unset I_MPI_STATS # ITAC doesn't use I_MPI_STATS. Enabling I_MPI_STATS will duplicated or double-work of tracing
- mpirun -n 8 -trace mpi_hello_world
- traceanalyzer mpi_hello_world.stf
