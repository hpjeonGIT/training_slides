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

## MATLAB standalone applications
- Instead of hard-coding basic parameters inside of the code, let matlab scripts read (fscanf) any external text file, enabling easy adjustment
- Conversion
  - Run >>> deploytool and select the appropriate menu
  - This may take more than 10 min
  - Will make the directory of the name of the matlab script/function, with 3 child directories of for_redistribution, for_testting, for_redistribution_files_only
- Installation of MATLAB runtime library
  - Running mcrinstaller in the matlab CLI shows where the zip file is located
  - Unzip and run “install” to install at a local directory
- From converted file, run as: ./app/for_testing/run_app.sh ~/sw_local/MATLAB_runtime/v85
- External files to be parsed in the matlab app are automatically included in the stand-alone application compilation
  - Even deleting the choice from the menu, it updates automatically anyway
  - Manually move such files from the folder temporarily
- Ref: https://www.mathworks.com/help/compiler_sdk/ml_code/mcr-component-cache-and-ctf-archive-embedding.html
  - In PBS script: SCRATCH_DIR=$WORK/$PBS_JOBID; mkdir $SCRATCH_DIR; export MCR_CACHE_ROOT=$SCRATCH_DIR ; 
  - Default MCR cache folder is located in $HOME/.mcrcache

## When graphics crashes due to opengl
- matlab -softwareopengl
