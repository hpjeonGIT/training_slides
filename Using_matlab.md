## Control the number of threads
- OMP_NUM_THREADS might be ignored
- maxNumCompThreads will be deprecated in future release
- feature('numThreads',str2num(getenv('OMP_NUM_THREADS')))
- or  feature('numThreads',6)
- matlab -singleCompThread will enforce to use one thread / one core only

## Checking License status
### Windows
- cd c:\program files\matlab2013a\etc\win64 (or installed directory)
- run “lmutil lmstat –a”
### Linux
/opt/apps/matlab/R2014a/etc/glnxa64/lmutil lmstat -a -c 27000@license_server

## Debugging in Linux CLI
- http://www.mathworks.com/help/matlab/matlab_external/debugging-on-linux-platforms.html
- matlab –Dgdb
- gdb> handle SIGSEGV SIGBUS nostop noprint 
- gdb> run –nojvm
- your_script (without .m extension)

# Making MATLAB code into DLL
-Install Windows SDK
  - May have to remove pre-installed VC++ 2010 redistribution
  - http://www.mathworks.com/matlabcentral/answers/95039-why-does-the-sdk-7-1-installation-fail-with-an-installation-failed-message-on-my-windows-system
- Run MATLAB
  - mex -setup
  - deploytool

## When graphics crashes due to opengl
- matlab -softwareopengl

<hr>
## Introduction to MATLAB standalone applications
### What is a stand-alone application?
- Your MATLAB script or program can be compiled using MATLAB compiler, running stand-alone - without MATLAB
	- This stand-alone requires MATLAB runtime library, which is free
	- No license required
	- Highly recommended for parametric study
- You can save licenses of MATLAB and toolboxes
- Stand-alone application might be faster than running from MATLAB platform

### Sample tutorial to produce a stand-alone application
- Prepare a text-based input file to control parameters. Save it as *input.txt*
```
#parpool
10
#Loop
100
#numThreads
4
#matrix size
1000
```
- Note that parpool size is 10 while numThreads is 4. We test on Atom cluster, which has 40 cpus per node as 10 parpool X 4 numthreads
- MATLAB script file is shown below. Save it as *run_test.m*
```
tic
fid = fopen('./input.txt');
line = fgetl(fid);line = fgetl(fid);npool = str2num(line)
line = fgetl(fid);line = fgetl(fid);nloop = str2num(line)
line = fgetl(fid);line = fgetl(fid);nthreads = str2num(line)
line = fgetl(fid);line = fgetl(fid);nsize = str2num(line)
fclose(fid);
feature('numThreads',nthreads)
parpool(npool)
a = zeros(nloop);
parfor i = 1:nloop
    a(i) = max(abs(eig(rand(nsize))));
end
sum(a)
poolobj = gcp('nocreate');
delete(poolobj);
toc
```
- This MATLAB scripts will execute eigen solver as many as nloop is required (dumb test). nloop is divided by par-for loop and each par-for loop will use nthreads for parallel eigen solver
- Steps to produce stand-alone application
	- Linux CLI
		- module load matlab
		- mcc -m run_test.m # this may take 1-2 min
			- Produces mccExcludedFiles.log, requiredMCRProducts.txt, run_run_test.sh,readme.txt,run_test
			- Distribute *run_run_test.sh* and *run_test binary* file
			- input.txt will be necessary to control inputs
	- MATLAB GUI
		- module load matlab
		- matlab
		- Run "deploytool" from MATLAB command line, and select Application Compiler
        - Select or include source files
        - Click Package
        - It may take a couple of minutes ...
        - Completed
        - Will produce 3 folders as 
        	- 1) for_redistribution: Installer enclosed
            - 2) for_redistribution_files_only: Executables and script. You may use as it is
            - 3) for_testing: might be slower than for_redistribution
		- ~~External files to be parsed in the matlab app are automatically included in the stand-alone application compilation~~
		- ~~Even deleting the choice from the menu, it updates automatically anyway~~
		- ~~Manually move such files from the folder temporarily~~

## Running MATLAB stand alone applications
- Command: 
	- *stand_alone_app.sh MATLAB_Runtime/vXX*
		- The version of MATLAB Runtime must match with the MATLAB which produced the stand-alone application
	- Sample command: *./run_run_test.sh /usr/local/matlab/MATLAB_Runtime/v95*
- Scratch space
	- A stand-alone application produces scratch files and appropriate adjustment is necessary for file IO and cleaning
	- Ref: https://www.mathworks.com/help/compiler_sdk/ml_code/mcr-component-cache-and-ctf-archive-embedding.html
	- Default MCR cache folder is located in $HOME/.mcrcache
    	- This could be a trouble when multiple stand-alone applications run. Use different MCR_CACHE_ROOT per PBS job
    	- Ex: *export MCR_CACHE_ROOT=/scratch/foo/tmp*
```bash
#!/bin/bash
#PBS -q @myserver
#PBS -l select=1:ncpus=20:mpiprocs=20
#PBS -l walltime=100:00:00
echo $PBS_O_WORKDIR
cd $PBS_O_WORKDIR
export TMPDIR=/scratch/$USER/tmp 
export SCRATCH=$TMPDIR/$PBS_JOBID
mkdir -p $SCRATCH
export  MCR_CACHE_ROOT=$SCRATCH
export V95LIB=/usr/local/matlab/MATLAB_Runtime/v95
export EXE=/home/foo/some_app/for_redistribution_files_only/run_my_app.sh 
$EXE $V95LIB  
```
- Note that the version of compiling MATLAB will determine the library of the stand-alone application. If the matlab code is compiled by 2018/b, then the stand alone application needs v95.
