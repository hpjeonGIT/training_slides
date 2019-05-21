- Basic command
	- For mode solutions: `mode-solutions`
	- For FDTD: `fdtd-solutions`
	- Checking license status: `lmutil lmstat -a -c portnumber@license_server`

- Coupling with MATLAB
	- Open mode-solutions or fdtd-solutions
	- Help -> Matlab integation status
	- In the Matlab Integration Configuration menu, enter the path of the loaded MATLAB
	- Restart mode-solutions or fdtd-solutions

- Batch processing
	- A sample script file, which is shown below, might be run as: `mode-solutions -exit -hide -run sample.lsf`
		- *exit(2)* exits the interactive menu of mode-solutions while it may not terminate the application
		- *-exit* terminates mode-solutions when batch script using *-run* is completed
```
?"Hello world.";
exit(2);
```
	- A sample PBS script is shown below
```
#!/bin/bash
#PBS -l select=1:ncpus=1:mpiprocs=1
#PBS -l walltime=1:00:00
#PBS -q @cluster_name
#PBS -N lumerical
cd $PBS_O_WORKDIR  
export NNODES=`sort $PBS_NODEFILE | uniq | wc -l`
export NPROCS=`wc -l < $PBS_NODEFILE`
. /etc/profile.d/modules.sh
#
module load lumerical
mode-solutions -exit -hide -run sample.lsf  -logfile log.out
```

- Trouble shootings
	- Mode-solutions in Lumerical writes scratch files or lock files of working models at $HOME/.cache/Lumerical/MODE-solutions
	- If `mode-solutions` GUI takes too much time to appear (more than a minute), clear cache files
