# VTune
- Profiling tool of Intel suite
- Can be coupled with mpirun
- VTUNE operation
  - $ source  /share/compiler/intel/18.0/vtune_amplifier_xe/amplxe-vars.sh intel64 (choose appropriate version of intel compiler using module load/unload)
  - GUI: amplxe-gui, pre/post, analysis can be done
  - CUI: amplxe-cl, collection/finalization can be deon. Analysis will require amplxe-gui
    - amplxe-cl -collect __collection_method__ -knob __sub_options__ -- __executable__
    - ex: amplxe-cl -collect hotspots -data-limit=200 myApp.exe
- Steps of VTUNE
  - Collection: Executing the code and receiving profile data. Can be run parallel (OpenMP, pthreads, MPI)
  - Finalization: Build database. Run as serial. Can be very slow.
  - For KNL: collection at KNL, and finalization/post-processing at Xeon
    - amplxe-cl -colle hotspots -finalization-mode=none ./md_sample # at KNL
    - amplxe-cl -finalize -result-dir ./r002hs -search-dir ./ # in Xeon
- Options
  - Collection method # might be changed by different versions
    - advanced-hotspots    Advanced Hotspots
    - concurrency          Concurrency
    - cpugpu-concurrency   CPU/GPU Concurrency
    - disk-io              Disk Input and Output
    - general-exploration  General Exploration
    - gpu-hotspots         GPU Hotspots
    - hotspots             Basic Hotspots
    - hotspots-0           Basic Hotspots 0
    - hpc-performance      HPC Performance Characterization
    - locksandwaits        Locks and Waits
    - memory-access        Memory Access
    - pyhotspots-0         Python Hotspots 0
    - sgx-hotspots         SGX Hotspots
    - tsx-exploration      TSX Exploration
    - tsx-hotspots         TSX Hotspots
  - Available suboptions (knob) : https://software.intel.com/en-us/node/544270#SAMPLING-INTERVAL

# Hotsopts 
- Basic profiling
- amplxe-cl -collect hotspots ./a.out
- Produces r00xhs folder
- amplxe-gui r000hs
  - Find the time around the loops, how much OMP threads are busy, efficiency of utilization, ...

# Advanced hotspots
- amplxe-cl -collect advanced-hotspots ./md_sample
- Produces r00xah folder
- amplxe-gui r000ah
  - N. of instructions retire, CPI (cycles per instruction), ....
  
# Memory bandwidth
- -collect memory-access and -collect general exploration may require root-adjustment
- Hardware event-based sampling is disabled. To enable, sep/sepdrv driver is needed
- Setting up driver
  - Using uncore events collection (not recommended though): 
    - sudo su root
    - echo 0 > /proc/sys/kernel/perf_event_paranoid
    - echo 0 > /proc/sys/kernel/kptr_restrict
    - This may blow the node
  - Running driver (might be recommended)
    - https://software.intel.com/en-us/vtune-amplifier-help-building-and-installing-the-sampling-drivers-for-linux-targets
    - sudo su root
    - cd /share/compiler/intel/18.0/
    - cd vtune_amplifier_xe/sepdk/src/
    - sudo ./build-driver
    - sudo ./insmod-sep -r -g MYGROUP # MYGROUP user group can use the driver
    - In order to stop the driver, sudo ./rmmod-sep -s
- Current configuration can be reveiweed using /share/compiler/intel/16.0/vtune_amplifier_xe/bin64/amplxe-runss --context-value-list
- When the driver is set
  - Basic command: amplxe-cl -collect memory-access ./a.out
  - Advanced command: 
    - Change sampling interval to reduce disk usage Also Dram bandwith limits are tested
    - amplxe-cl -collect memory-access -knob analyze-mem-objects=true -knob dram-bandwidth-limits=true -knob sampling-interval=100 ./a.out
  - This will produce r000macc folder
    - Check memory bandwidth - MAX DRAM bandwidth ~ 110GB

# VTune for MPI code
- amplxe-cl -collect hotspots mpirun -n 8 ./a.out
  - Produces r000hs
  - Aggregated MPI function calls
- mpirun -n 8 amplxe-cl -collect hotspots -result-dir=./VT ./a.out
  - Produces .VT.$HOSTNAME folder and results per rank
  - Aggregated but discernable by MPI ranks





