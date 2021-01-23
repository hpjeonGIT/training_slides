
## Basic command
- ifort: Intel fortran compiler
- icc: Intel C compiler
- icpc: Intel C++ compiler
- When Intel MPI is enabled
  - source <intel_install_path>/impi/2019.1.144/intel64/bin/mpivars.sh
	- mpicc: Intel MPI with gcc
	- mpicxx: Intel MPI with g++
	- mpif77/mpif90: Intel MPI with gfortran
	- mpiicc: Intel MPI with icc
	- mpiicpc: Intel MPI with icpc
	- mpiifort: intel MPI with ifort
- Intel MKL libraries: source <intel_install_path>/mkl/bin/mklvars.sh intel64
- Intel VTune profiler: source <intel_install_path>/vtune_amplifier/amplxe-vars.sh
- Intel Vectorization advisor: source <intel_install_path>/advisor/advixe-vars.sh
- Intel Trace Analyzer and Collector: source <intel_install_path>/itac_latest/bin/itacvars.sh

## Compiling option
- -g: enabling debug mode
- -check bounds: checks if any index violates the size of array
- -fpe0: checks division by zero
- -O0/-O1/-O2/-O3: no/level-1/level-2/level-3 optimization
- -xHost: reads /proc/cpuinfo and optimizes the code using available instructions. Highly aggresive optimization
- -no-vec/-xsse2/-xavx/-xavx2: no vectorization/vectorization using sse2/AVX vectorization/AVX2 vectorization
	- AVX2 is not supported in sc1000/Focus clusters. Check /proc/cpuinfo of every cluster
- -xCore-AVX512/-xCOMMON-AVX512: optimization using core/common AVX512 instructions
	- AVX512 is supported in Vector/Atom cluster. However, if the code is not specifically written for AVX512, enabling AVX512 might not be encouraged
	- Don't guess. MEASURE IT.
- -ipo: Inter-procedural optimization. Highly recommended
- -fp-model: Adjusts floating-point model
- -Ofast: combination of -O3 -no-prec-div -fp-model fast=2
- -mkl: using MKL library. *-mkl=parallel* is default. For serial MKL library, use *-mkl=sequential*
- -qopenmp/-fopenmp: enabling OpenMP
- -parallel: enabling auto-parallelization
- Sample optimization commands
	- ifort -O3 -xHost -fp-model fast=2 -ipo ex.f90
	- icc -xavx2 -Ofast -ipo ex.c
- Aggressive optimization may hurt the accuracy. Do sanity check always
- Aggressive optimization may hurt the performance
	- Again: Don't guess. MEASURE IT

# Some guide for code optimization using compiler options
- Check /proc/cpuinfo and find any vector instructions can be used: avx, avx2, avx512, ...
- Compile the code naively using -O0 or -O1, without vectorization. Test and get results
- Increase the level of optimization like -O2 or -O3. If you have significantly different results b/w -O1 and -O2, your code may have serious bugs
- From -O0 to -O3, if everything works good then try vectorization and interprocedural optimization
	- Benchmark with or without -ipo/avx/avx2/xhost/fp-model fast=1,2... and find the best combination
	- Results must not yield significant differences like less than 0.1 % after 1000 steps in total energy (or main result) when compared to -O0 or -O1 naively compiled ones
	- Again: Don't guess. MEASURE IT
- Performance gain less than 30% would be errorneous or trivial
- In order to find average wall time, repeat 5-10 times of run

# Using preprocessor for icpc
- icpc -E somesource.cpp > test.i
- This may show what header files are missing
