- Commands
	- Load Rsoft environment
	- `rslmd -start`
	- `xfullwave`
		- Or other Rsoft modules
	- `rslmd -stop`
	- Checking license status: `lmutil lmstat -a -c  port_number@license_server`

- Distributed computing of fullwave
	- `rslmd -start`
	- `export P4_RSHCOMMAND=rshlocal`
	- `fwmpirun -np 4 sample.ind`
	- `rslmd -stop`
	- A sample PBS script is shown below
```
#!/bin/bash
#PBS -l walltime=10:00:00
#PBS -l select=2:ncpus=32:mpiprocs=32
#PBS -q @cluster_name
#PBS -N rsoftfullwave
################# DO NOT EDIT BELOW ############
. /etc/profile.d/modules.sh
export NNODES=`sort $PBS_NODEFILE | uniq | wc -l`
export NPROCS=`wc -l < $PBS_NODEFILE`
################## DO NOT EDIT ABOVE ###########
cd $PBS_O_WORKDIR
module load rsoft
rslmd -start
export P4_RSHCOMMAND=rshlocal
fwmpirun -np $NPROCS -hosts $PBS_NODEFILE sample.ind
rslmd -stop
```

- Trouble shooting
	- Default configuration is stored in *$HOME/.xbcad.ini*
	- If `fwmpirun` doesn't work, remove or disable the current *.xbcad.ini*
