# Profiling
- Examine the program/source code to check how much computing resource is consumed in each subroutine/function/line
- Why profiling?
    - Optimize the code to run faster or more efficiently
    - You don’t need to optimize all of the codes
- Pareto principle (or 80-20 rule)
    - 80% of computing resource is taken at 20% of the source code
    - Or 90-10
- Profiling tells you where to optimize

# Basics of code optimization
- Avoid multiples of same operation
- Use temporary memory or space
    - sin/cos/exp/erf/pow(**) are extremely expensive
    - z^5 + z^3 + z => z*(1.0 + z*z*(1.0+z*z))
- Simplify algorithm
    - Implement (final) analytic solution
    - Force is the derivative of potential. Do not differentiate Potential results in the code. Instead, implement the equations of force by differenitating potential equations.
- Use exact/appropriate memory
    - Too big memory allocation will waste RAM/cache/IO/…
    - Reduce problem size as small as possible
    - No garbage collection in Fortran/C/C++

# How to Profile?
### In CPU-time wise
- Mechanically measure how much time is taken between the routine or functions
```bash
do loop
	a_time = time()  # initial time
	do_some_heavy_jobs
	b_time = time() – a_time # time consumed
	time_agg = time_agg + b_time  # aggregate results
end loop
```
    - in fortran: secnds(), omp_get_wtime(), mpi_wtime()
    - in python: time.time()
    - Analyze using the aggregated results (more than 100~1000), not a single shot
- Or use profiler
### Memory wise
- Use open-source (valgrind) or commercial tools

# Common profilers
- gprof
    - GNU profiler
    - CLI
- Vtune
    - Intel composer package
    - Can track up to every line
- MAP
    - Allinea
    - Highly recommended

# Using gprof
- Compile and link with –pg option
    - gfortran –pg –g –O3 md.f
- Run the executable
    - ./a.out
    - gmon.out is produced
- Run gprof
    - gprof ./a.out > log.out
- Read log.out
```console
Flat profile:

Each sample counts as 0.01 seconds.
  %   cumulative   self              self     total           
 time   seconds   seconds    calls   s/call   s/call  name    
 91.21      1.61     1.51    20000     0.00     0.00  ***_
  2.39      1.75     0.04    20000     0.00     0.00  ****_
  
 %         the percentage of the total running time of the
time       program used by this function.

cumulative a running sum of the number of seconds accounted
 seconds   for by this function and those listed above it.

 self      the number of seconds accounted for by this
seconds    function alone.  This is the major sort for this
           listing.

```

# What is a debugger?
- A tool to help and fix your program codes
- Can run your code line-by-line
- Can locate a crashing point
- Can track values of variables to examine
- But may not help you to find out logical bugs

# Common debuggers
- gdb
    - Open-source
    - Can debug MPI code
    - (maybe) not-fancy
- ddt
    - Allinea/armforge
    - Powerful MPI debugger !!!
    - De-facto standard in many National Laboratory clusters

# How to use gdb
- Compile with –g option
    - ifort –g hello.f90
- Run gdb
```console
# gdb ./a.out
(gdb)
When standard input is required
(gdb) run < input.txt
Some commands
(gdb) b main.f90:48
(gdb) run
(gdb) p a_t
(gdb) n
```
- Compile mpi code
    - mpifort –g hello_mpi.f90
- Running gdb with mpi
    - mpirun –n 2 xterm –e gdb ./a.out

# How to use armforge ddt
- Compile the source code with –g option
    - ifort –g –O3 hello.f90
- Run ddt
    - ddt ./a.out
- Compiling mpi code
    - mpifort –g hello_mpi.f90
- Running ddt
    - ddt ./a.out

# Using valgrind
- memory leak check: mpirun -np 4 valgrind --quiet --tool=memcheck --leak-check=yes --leak-resolution=high --track-origins=yes -
-show-reachable=yes --num-callers=50 ./a.out
- massif for memory consumption: mpirun -np 4 valgrind --tool=massif  ./a.out
	- This will produce massif.out.PID files. No MPI rank information
	- May use massif-visualizer: https://milianw.de/tag/massif-visualizer
