# OpenMP
- Introduction
	- Multiple threading parallelism in CPU
		- Only on a single node of SMP
		- Using the shared memory among multiple processors
		- Can be coupled with MPI/OpenACC
		- Can be coupled with vectorization
	- Inject "sentinel" arround the loops
		- Tells the compiler the ROI for parallelism
		- Private/Shared variables for each thread
		- Single thread or synchronization using atomic or critical section
		- Reduce operation for scalar variables
			- No array or vectors
		- Nested loops or parallelism supported
			- Multiple steps of parallelism
	- Mostly better than auto-parallelization
		- When the loop is complex

- Using OpenMP
	- Inject sentinels in the top and bottom of the loop
		- Decide private/shared variables for the ones used inside the loop
	- Compile the source code using 
		- -fopenmp for GCC
		- -fopenmp or -qopenmp for Intel compiler
	- Configure the number of threads to use
		- export OMP_NUM_THREADS=8
		- ./a.out
	- Rule of thumb
		- Mostly MPI parallelism is better than OpenMP or multiple-threading
		- But hybrid parallelism might be better than bare MPI when CPU density per NIC is high
		- Sweet-spot of OpenMP is 8-12 threads
  		- Dont' guess, MEASURE IT
	- Sample compilation options
		- Intel
			- ver< 2017: ifort -Ofast -openmp omp.f90
			- ver >= 2017: ifort -Ofast -qopenmp omp.f90
		- PGI
			- pgf90 -fast -mp omp.f90
- Sample code
	- Bare
```c
void force(particle *q)
{
  unsigned i, j, k;
  double r2, dx[3], coef, x;
  /* force initialization */
  for(i=0; i<Npt; i++) for (k=0;k<3;k++) q[i].ff[k] = 0.0;
  /* coupled loop for many-body interaction */
  for (i=0; i<Npt-1; i++) {
    for (j=i+1; j<Npt; j++) {
      r2 = 0.0;
      for (k=0; k<3; k++) {
	x = q[i].xx[k] - q[j].xx[k];
	dx[k] = x - box * dnint(x/box);
	r2 += dx[k]*dx[k];
      }
      if (r2 < rcut2) {
	coef = 1./(r2*sqrt(r2));
	for (k=0; k<3; k++) {
	  q[i].ff[k] += coef * dx[k];
	  q[j].ff[k] -= coef * dx[k];
	}
      }
    }
  }
}
```
	- OMP version. Note how the thread conflict is avoided
```c
void force_omp(particle *q)
{
    unsigned i, j, k;
    double r2, dx[3], coef, x;
    double **tmp;
/* force initialization */
    for(i=0; i<Npt; i++) for (k=0;k<3;k++) q[i].ff[k] = 0.0;
/* coupled loop for many-body interaction */
#pragma omp parallel default(shared) private(tmp, i, k)
    {
	tmp = malloc(Npt*sizeof **tmp);
	for (i=0;i<Npt;i++) tmp[i] = malloc(3*sizeof *tmp);
	for (i=0;i<Npt;i++) for (k=0;k<3;k++) tmp[i][k] = 0.0;
#pragma omp for private(j,r2,x,dx,coef)
	for (i=0; i<Npt-1; i++) {
	    for (j=i+1; j<Npt; j++) {
		r2 = 0.0;
		for (k=0; k<3; k++) {
		    x = q[i].xx[k] - q[j].xx[k];
		    dx[k] = x - box * dnint(x/box);
		    r2 += dx[k]*dx[k];
		}
		if (r2 < rcut2) {
		    coef = 1./(r2*sqrt(r2));
		    for (k=0; k<3; k++) {
			tmp[i][k] += coef * dx[k];
			tmp[j][k] -= coef * dx[k];
		    }
		}
	    }
	}
#pragma omp critical
	{
	    for (i=0;i<Npt;i++) for (k=0;k<3;k++) q[i].ff[k] += tmp[i][k];
	}
	for (i=0;i<Npt;i++) free(tmp[i]);
	free(tmp);
    }
}
```

# OpenACC
- Introduction
	- Assume that you use PGI compiler
	- Developed for GPGPU computing
	- But CPU can use OpenACC !
		- -ta=multicore for CPU
		- OMP_NUM_THREADS may conflict with CGROUP
		- export MP_BLIST=0,1,2,3,4,5
	- More abstract than CUDA
		- CUDA is extremely hard to use
	- Fortran/C/C++ supported
		- PGI and GCC compiler
		- Can be coupled with OpenMP/MPI
	- Similar feeling and look of OpenMP
		- OpenMP-style parallelism (or vectorization) on GPGPU
		- More explicit than OpenMP
			- Can configure which GPU will be used
		- Don't guess. MEASURE IT

- Using OpenACC
	- Needs GPGPU on the node
	- PGI compiler is recommended
	- Compile the source code using 
		- -fopenacc for GCC
		- -acc for PGI compiler
			- -ta=tesla for GPU, -ta=multicore for CPU
	- Monitor GPU status using command: *nvidia-smi -l*
	-Ref:
		- http://web.stanford.edu/class/cme213/files/lectures/Lecture_14_openacc2017.pdf
		- https://www.pgroup.com/resources/docs/18.3/pdf/openacc18_gs.pdf
	- Issues
		- Derived data type is not supported
		- Multi-dimesional array is not supported
		- MultiGPU support is limited
			- One MPI rank per GPU is recommended
	- Key words
		- gang => thread block
		- worker => warp
		- vector => thread

- Comparison of OpenMP and OpenACC implementation
	- Simple OpenMP routine
		- pgf90 -mp -fast ex.f90
			- 48 sec with 24 threads
```fortran
subroutine cpu_loop(a,b,n,niter)
  implicit none
  integer:: n, niter, i, j,k
  real*8:: a(n,n), b(n,n), w0, w1, w2
  w0 = 1.01d0
  w1 = 1.02d0
  w2 = 0.98d0
  do k=1, niter
     !$omp parallel &
     !$omp default(shared) &
     !$omp private(i,j)
     !$omp do &
     !$omp schedule(static) 
     do i=2, n-1
        do j=2, n-1
           b(i,j) = w0*(a(i,j)   + a(i-1,j)   + a(i+1,j))+ &
                &   w1*(a(i,j+1) + a(i-1,j+1) + a(i+1,j+1)) + &
                &   w2*(a(i,j-1) + a(i-1,j-1) + a(i+1,j-1))
        end do
     enddo     
     !$omp end do
     !$omp end parallel
  end do
  return
end subroutine cpu_loop
```
	- OpenACC sample routine
		- pgf90 -acc -fast ex.f90
		- 7 sec using p100
```fortran
subroutine gpu_loop(a,c,n,niter)
  implicit none
  integer::n, niter, i, j,k
  real*8:: a(n,n), c(n,n), w0, w1, w2
  w0 = 1.01d0
  w1 = 1.02d0
  w2 = 0.98d0
  !$acc data copy(c(:,:)) copyin(a(:,:))
  do k=1, niter
     !$acc kernels loop private(i,j)
     do i=2, n-1
        do j=2, n-1
           c(i,j) = w0*(a(i,j)   + a(i-1,j)   + a(i+1,j))+ &
                &   w1*(a(i,j+1) + a(i-1,j+1) + a(i+1,j+1)) + &
                &   w2*(a(i,j-1) + a(i-1,j-1) + a(i+1,j-1))
        end do
     enddo
  end do
  !$acc end data
  return
end subroutine gpu_loop
```

- Effect of GPU memory copy in/out frequency
	- Calling a/b computing every iteration
		- GPU copy in/out done every loop
		- 290 sec
```fortran
...
  niter=100; npiece=5
  call cpu_time(t0)
  do i=1, niter*npiece
     call every_loop(a,b,n)
  end do
  call cpu_time(t1)
  print *, "every loop = ", t1-t0
...
subroutine every_loop(a,c,n)
  implicit none
  integer::n, i, j,k
  real*8:: a(n,n), c(n,n), w0, w1, w2
  w0 = 1.01d0
  w1 = 1.02d0
  w2 = 0.98d0
  !$acc data copy(c(:,:),a(:,:))
  !$acc kernels loop  private(i,j)
  do i=2, n-1
     do j=2, n-1
        c(i,j) = w0*(a(i,j)   + a(i-1,j)   + a(i+1,j))+ &
             &   w1*(a(i,j+1) + a(i-1,j+1) + a(i+1,j+1)) + &
             &   w2*(a(i,j-1) + a(i-1,j-1) + a(i+1,j-1))
     end do
  enddo
  !$acc kernels loop private(i,j) 
  do i=2, n-1
     do j=2, n-1
        a(i,j) = w0*(c(i,j)   + c(i-1,j)   + c(i+1,j))+ &
             &   w1*(c(i,j+1) + c(i-1,j+1) + c(i+1,j+1)) + &
                &   w2*(c(i,j-1) + c(i-1,j-1) + c(i+1,j-1))
     end do
  enddo
  !$acc end data
end subroutine
```
	- Calling a/b computing with a chunk of iterations (=100)
		- GPU copy in/out done every 100
		- 9 sec
```fortran
...
call cpu_time(t0)
  do i=1, npiece
     call chunk_loop(d,c,n,niter)
  end do
  call cpu_time(t1)
  print *, "every 100 loop = ", t1-t0
...
subroutine chunk_loop(a,c,n,niter)
  implicit none
  integer::n, niter, i, j,k
  real*8:: a(n,n), c(n,n), w0, w1, w2
  w0 = 1.01d0
  w1 = 1.02d0
  w2 = 0.98d0
  !$acc data copy(c(:,:),a(:,:))
  do k=1, niter
     !$acc kernels loop  private(i,j)
     do i=2, n-1
        do j=2, n-1
           c(i,j) = w0*(a(i,j)   + a(i-1,j)   + a(i+1,j))+ &
                &   w1*(a(i,j+1) + a(i-1,j+1) + a(i+1,j+1)) + &
                &   w2*(a(i,j-1) + a(i-1,j-1) + a(i+1,j-1))
        end do
     enddo
     !$acc kernels loop private(i,j) 
     do i=2, n-1
        do j=2, n-1
           a(i,j) = w0*(c(i,j)   + c(i-1,j)   + c(i+1,j))+ &
                &   w1*(c(i,j+1) + c(i-1,j+1) + c(i+1,j+1)) + &
                &   w2*(c(i,j-1) + c(i-1,j-1) + c(i+1,j-1))
        end do
     enddo
  end do
  !$acc end data
  return
end subroutine chunk_loop
```

- Discussion
	- Use -Minfo=accel to figure out the status of vectorization
	- Don't guess, MEASURE IT
	- Coupling with MPI is highly recommended for multi-GPU computing
	- In C, restrict pointer is necessary
	- STL is under test for C++
