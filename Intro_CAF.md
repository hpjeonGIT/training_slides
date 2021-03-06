# Sample code
- Ref: https://github.com/shawfdong/hyades/wiki/Coarray-Fortran
```fortran
program caf_hello

  character*80 hostname
  call hostnm(hostname)
  write(*,*) "Hello from image ", this_image(), &
             "running on ", trim(hostname), &
             " out of ", num_images()

end program caf_hello
```

# Compiling as SMP in intel compiler
- ifort -coarray caf_hello.f90 -o caf_hello.x
- export FOR_COARRAY_NUM_IMAGES=4
- ./caf_hello.x
# Compiling as Distributed mode in intel compiler
- Prepare xx.conf: -machinefile hosts -genvall -genv I_MPI_FABRICS shm:ofa -n 4 ./caf_hello.dist
- ifort -coarray=distributed -coarray-config-file=xx.conf caf_hello.f90  -o caf_hello.dist
- Prepare hosts file
- ./caf_hello.dist
- Intel fortran does not support CAF fully
- CO_SUM() is not available in 18

# Another example
- Ref: https://sourceforge.net/p/coarrays/svn/71/tree//head/doc/doc.pdf?format=raw
- Internal fuctions
  - this_image(), num_images(), sync images()/all
- Sample PI code
```fortran
program caf_pi
  implicit none
  integer :: j
  integer :: seed(2)
  integer*8 :: N_steps, i_step, hits
  double precision :: x, y
  double precision :: pi_sum, pi
  double precision :: pi_global[*]
  seed(1) = 17*this_image()
  if (this_image() == 1) then
     print*, 'num images = ', num_images()
  end if
  call random_seed(put=seed)
  hits = 0_8
  N_steps = 10000000_8
  do i_step=1_8, N_steps
     call random_number(x)
     call random_number(y)
     if ( (x*x + y*y) <= 1.d0) then
        hits = hits + 1_8
     endif
  enddo
  pi_global = 4.d0*dble(hits)/dble(N_steps)
  SYNC ALL
  if (this_image() == 1) then
     pi_sum = 0.d0
     do j=1,num_images()
        pi_sum = pi_sum + pi_global[j]
     enddo
     pi = pi_sum / num_images()
     print *, 'pi = ', pi
  endif
end program caf_pi
```
# Compiling as SMP
- ifort -coarray pi.f90
- export FOR_COARRAY_NUM_IMAGES=6
- ./a.out
# Compiling for Distributed computing
- Prepare caf.conf:
   -machinefile hosts -genvall -genv I_MPI_FABRICS shm:ofa -n 6  ./a.out
- ifort -coarray=distributed -coarray-config-file=caf.conf pi.f90
- ./a.out
- Ref: http://pleiades.ucsc.edu/ams250/2017/lectures/Lecture-30-PGAS.pdf

# Nitty Gritty
- Ref: http://www.training.prace-ri.eu/uploads/tx_pracetmo/L04_Experiences.pdf
  - Sync all -> sync images (image) or sync images (image_list)
  - Synchronization might be expensive
  - Use MPI for collectives when MPI+coarrays are supported
- Ref: https://github.com/sourceryinstitute/OpenCoarrays/issues/349
  - MPI_init() and MPI_finalize() are handled by CAF_INIT(), which is not adjustable by a developer
  - Just call MPI_COMM_RANK() and and MPI_COMM_SIZE(), skipping MPI_INIT/Finalize()
  - Use OpenCoarray for better performance
  - https://groups.google.com/forum/#!topic/comp.lang.fortran/5fsf-Mx79CU
