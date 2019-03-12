# Using LSDYNA CLI
- lstc_qrun # shows the current license status
- lstc_qkill processid@machine_name # when terminating the current LSDYNA process. Ctrl-C may not clean the license consumption
- Sample command:
    - mpp_s memory=1000M i=input.k
    - mpirun -np 32 mpp_d i=boot.k ncpu=32
- lsprepost # for pre-post

# Batch job example
```bash
#!/bin/bash
#PBS -l select=1:ncpus=32:mpiprocs=32
#PBS -l walltime=1:00:00
#PBS -q @apollo
#PBS -N LSDYNA

cd $PBS_O_WORKDIR

export NNODES=`sort $PBS_NODEFILE | uniq | wc -l`
export NPROCS=`wc -l < $PBS_NODEFILE`

. /etc/profile.d/modules.sh
module load LS-DYNA
mpirun -np ${NPROCS}  mpp_d  i=boot.k  ncpu=${NPROCS}
```
