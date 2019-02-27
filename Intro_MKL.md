# MKL
- Math Kernel Library
  - Numerical library by Intel
  - MKL library is free to download
  - Encloses blas, lapack, scalapack
- How to use
  - ifort –mkl=sequential …
  - icc –mkl=parallel …

# Matrix solver
- Solve A*B=C
  - A = NxN matrix
  - B = N vector, objectives or unknown
  - C = N vector
  - B = A^-1*C
- Matrix A
  - Symmetric?
  - Hermitian?
  - Banded?
  - Sparse or dense?
  - Positive definite?

# DGESV
- Dense matrix solver
- With intel mkl library
  - ifort –mkl using_dgesv.f90
  - ifort –mkl=sequential using_dgesv.f90
  - ifort –mkl=parallel using_dgesv.f90
```fortran
program matrix_solver_dgesv
implicit none
  INTEGER, PARAMETER :: dp = KIND(1.0D0)
  INTEGER N, NRHS
  INTEGER, ALLOCATABLE :: IPIV(:)
  REAL(KIND=DP), ALLOCATABLE :: A(:,:), B(:), oldA(:,:)
  INTEGER:: i, LDA, LDB, INFO, ierr
  !
  N = 16
  allocate(A(N,N), IPIV(N), B(N), oldA(N,N), stat= ierr)
  A = reshape ((/3.4225E-08,-1.7112E-08,0,0,-1.7113E-08,0,0,0,0,0,0,0,0,0,0,0, &
     & -1.7112E-08,3.4223E-08,-1.7112E-08,0,0,-1.225E-15,0,0,0,0,0,0,0,0,0,0, &
     & 0,-1.7112E-08,5.1337E-08,-1.7112E-08,0,0,-1.7113E-08,0,0,0,0,0,0,0,0,0,&
     & 0,0,-1.7112E-08,3.4225E-08,0,0,0,-1.7113E-08,0,0,0,0,0,0,0,0,&
     & -1.7113E-08,0,0,0,3.4228E-08,-1.225E-15,0,0,-1.7115E-08,0,0,0,0,0,0,0,&
     & 0,-1.225E-15,0,0,-1.225E-15,4.9E-15,-1.225E-15,0,0,-1.225E-15,0,0,0,0,0,0,&
     & 0,0,-1.7113E-08,0,0,-1.225E-15,5.1341E-08,-1.7113E-08,0,0,-1.7115E-08,0,0,0,0,0,&
     & 0,0,0,-1.7113E-08,0,0,-1.7113E-08,5.1341E-08,0,0,0,-1.7115E-08,0,0,0,0,&
     & 0,0,0,0,-1.7115E-08,0,0,0,5.1344E-08,-1.7114E-08,0,0,-1.7115E-08,0,0,0,&
     & 0,0,0,0,0,-1.225E-15,0,0,-1.7114E-08,5.1343E-08,-1.7114E-08,0,0,-1.7115E-08,0,0,&
     & 0,0,0,0,0,0,-1.7115E-08,0,0,-1.7114E-08,6.8457E-08,-1.7114E-08,0,0,-1.7115E-08,0,&
     & 0,0,0,0,0,0,0,-1.7115E-08,0,0,-1.7114E-08,5.1343E-08,0,0,0,-1.7115E-08,&
     & 0,0,0,0,0,0,0,0,-1.7115E-08,0,0,0,5.7048E-08,-2.2819E-08,0,0,&
     & 0,0,0,0,0,0,0,0,0,-1.7115E-08,0,0,-2.2819E-08,7.9867E-08,-2.2819E-08,0,&
     & 0,0,0,0,0,0,0,0,0,0,-1.7115E-08,0,0,-2.2819E-08,7.9866E-08,-2.2818E-08,&
     & 0,0,0,0,0,0,0,0,0,0,0,-1.7115E-08,0,0,-2.2818E-08,5.7047E-08/), (/N,N/))
  B = reshape((/2.538E-09, 2.538E-09, 2.538E-09, 2.538E-09, 2.538E-09, 2.538E-09,&
       & 2.538E-09, 2.538E-09, 2.538E-09, 2.538E-09, 2.538E-09, 2.538E-09, &
       & 2.538E-09, 2.538E-09, 2.538E-09, 2.538E-09/), (/16/))
  oldA = A
  ! Regular dense matrix solver
  NRHS = 1
  LDA = N
  LDB = N
  CALL DGESV( N, NRHS, A, LDA, IPIV, B, LDB, INFO )
  ! A and B are changed
  do i =1, N
     print '(ES11.4 )', B(i)
  end do
  print *, matmul(oldA, B)
deallocate(A, IPIV, B, oldA, stat=ierr)
end program matrix_solver_dgesv
```

# PARDISO
- (Parallel) sparse matrix solver
- Assuming an indefinite matrix
  - Mtype=-2
- Conversion to CSR format is necessary
- With Intel MKL
  - ifort –mkl using_pardiso.f90

```fortran
  include 'mkl_pardiso.f90'
program using_pardiso
  use mkl_pardiso
  IMPLICIT NONE
  INTEGER, PARAMETER :: dp = KIND(1.0D0)
  TYPE(MKL_PARDISO_HANDLE), ALLOCATABLE  :: pt(:)
  INTEGER maxfct, mnum, mtype, phase, n, nrhs, error, msglvl
  INTEGER, ALLOCATABLE :: iparm(:), ia(:), ja(:), jx(:)
  REAL(KIND=DP), ALLOCATABLE :: aa(:), A(:,:), ax(:), B(:), x(:)
  INTEGER:: i, idum(1),j, jcnt, ierr
  REAL(KIND=DP) ddum(1)

  N = 16
  allocate(A(N,N), ax(N*N), ia(N+1), jx(N*N), B(N), stat=ierr)

  ! banded matrix - depends on the problem
  A = reshape ((/3.4225E-08,-1.7112E-08,0,0,-1.7113E-08,0,0,0,0,0,0,0,0,0,0,0, &
     & -1.7112E-08,3.4223E-08,-1.7112E-08,0,0,-1.225E-15,0,0,0,0,0,0,0,0,0,0, &
     & 0,-1.7112E-08,5.1337E-08,-1.7112E-08,0,0,-1.7113E-08,0,0,0,0,0,0,0,0,0,&
     & 0,0,-1.7112E-08,3.4225E-08,0,0,0,-1.7113E-08,0,0,0,0,0,0,0,0,&
     & -1.7113E-08,0,0,0,3.4228E-08,-1.225E-15,0,0,-1.7115E-08,0,0,0,0,0,0,0,&
     & 0,-1.225E-15,0,0,-1.225E-15,4.9E-15,-1.225E-15,0,0,-1.225E-15,0,0,0,0,0,0,&
     & 0,0,-1.7113E-08,0,0,-1.225E-15,5.1341E-08,-1.7113E-08,0,0,-1.7115E-08,0,0,0,0,0,&
     & 0,0,0,-1.7113E-08,0,0,-1.7113E-08,5.1341E-08,0,0,0,-1.7115E-08,0,0,0,0,&
     & 0,0,0,0,-1.7115E-08,0,0,0,5.1344E-08,-1.7114E-08,0,0,-1.7115E-08,0,0,0,&
     & 0,0,0,0,0,-1.225E-15,0,0,-1.7114E-08,5.1343E-08,-1.7114E-08,0,0,-1.7115E-08,0,0,&
     & 0,0,0,0,0,0,-1.7115E-08,0,0,-1.7114E-08,6.8457E-08,-1.7114E-08,0,0,-1.7115E-08,0,&
     & 0,0,0,0,0,0,0,-1.7115E-08,0,0,-1.7114E-08,5.1343E-08,0,0,0,-1.7115E-08,&
     & 0,0,0,0,0,0,0,0,-1.7115E-08,0,0,0,5.7048E-08,-2.2819E-08,0,0,&
     & 0,0,0,0,0,0,0,0,0,-1.7115E-08,0,0,-2.2819E-08,7.9867E-08,-2.2819E-08,0,&
     & 0,0,0,0,0,0,0,0,0,0,-1.7115E-08,0,0,-2.2819E-08,7.9866E-08,-2.2818E-08,&
     & 0,0,0,0,0,0,0,0,0,0,0,-1.7115E-08,0,0,-2.2818E-08,5.7047E-08/), (/N,N/))
  B = reshape((/2.538E-09, 2.538E-09, 2.538E-09, 2.538E-09, 2.538E-09, 2.538E-09,&
     & 2.538E-09, 2.538E-09, 2.538E-09, 2.538E-09, 2.538E-09, 2.538E-09, &
     & 2.538E-09, 2.538E-09, 2.538E-09, 2.538E-09/), (/16/))

! Making CSR format: https://en.wikipedia.org/wiki/Sparse_matrix
  jcnt = 0
  do i=1, N
     ia(i) = jcnt + 1
     do j=i, N
        if (dabs(A(i,j)) > 1.e-30 .or. i==j) then
           jcnt = jcnt + 1
           ax(jcnt) = A(i,j)
           jx(jcnt) = j
        end if
     end do
  end do
  ia(N+1) = jcnt + 1

  allocate(ja(jcnt), aa(jcnt))
  ja(1:jcnt) = jx(1:jcnt)
  aa(1:jcnt) = ax(1:jcnt)
  deallocate(jx,ax)
  allocate(pt(64), iparm(64),x(N), stat=ierr)
  DO i = 1, 64
     pt(i)%DUMMY =  0 
  END DO
  
  nrhs = 1
  maxfct = 1
  mnum = 1
  iparm = 0
  iparm(1) = 1 ! no solver default
  iparm(2) = 2 ! fill-in reordering from METIS
  iparm(3) = 1 ! OMP_NUM_THREADS
  iparm(6) = 0
  iparm(10) = 13 ! perturbe the pivot elements with 1E-13
  iparm(11) = 1 ! use nonsymmetric permutation and scaling MPS
  iparm(13) = 2 ! use nonsymmetric permutation and scaling MPS
  iparm(18) = -1 ! Output: number of nonzeros in the factor LU
  iparm(19) = -1 ! Output: Mflops for LU factorization  !
  iparm(21) = 1
  error = 0 ! initialize error flag
  msglvl = 1 ! print statistical information = 1
  mtype = -2 ! 1 for real/symm, 2 for real/symm/pos def, -2 for real/sym/indef
  phase = 11 ! only reordering and symbolic factorization
  call pardiso(pt, maxfct, mnum, mtype, phase, n, aa, ia, ja, &
       & idum, nrhs, iparm, msglvl, ddum, ddum, error)
  WRITE(*,*) 'Reordering completed ... '
  IF (error .NE. 0) THEN
     WRITE(*,*) 'The following ERROR was detected: ', error
     STOP
  END IF
   phase = 22 ! only factorization
  CALL pardiso (pt, maxfct, mnum, mtype, phase, n, aa, ia, ja, &
       & idum, nrhs, iparm, msglvl, ddum, ddum, error)
  iparm(8) = 15 ! max numbers of iterative refinement steps
  phase = 33 ! only factorization
  CALL pardiso (pt, maxfct, mnum, mtype, phase, n, aa, ia, ja, &
       & idum, nrhs, iparm, msglvl, b, x, error)
  phase = -1 ! release internal memory
  CALL pardiso (pt, maxfct, mnum, mtype, phase, n, ddum, idum, &
       & idum,idum, nrhs, iparm, msglvl, ddum, ddum, error)
     
  WRITE(*,*) 'The solution of the system is '
  DO i = 1, n
     WRITE(*,*) ' x(',i,') = ', x(i)
  END DO

  print *, matmul(A, x)
end program using_pardiso
```

# DSS
- Another sparse solver in MKL
  - Might not be parallel
- Conversion to CSR format is necessary
- With Intel MKL
  - ifort –mkl using_dss.f90

```fortran
program using_dss
  IMPLICIT NONE
  include 'mkl_dss.fi'
  INTEGER, PARAMETER :: dp = KIND(1.0D0)
  !.. All other variables
  INTEGER error, N,NRHS
  INTEGER, ALLOCATABLE :: ia(:), ja(:), jx(:)
  REAL(KIND=DP), ALLOCATABLE :: aa(:), A(:,:), ax(:), B(:), x(:)
  INTEGER:: i, idum(1),j, jcnt, ierr
  INTEGER*8:: handle
  REAL(KIND=DP) ddum(1)

  N = 16
  allocate(A(N,N), ax(N*N), ia(N+1), jx(N*N), B(N), x(N), stat=ierr)
  A = reshape ((/3.4225E-08,-1.7112E-08,0,0,-1.7113E-08,0,0,0,0,0,0,0,0,0,0,0, &
     & -1.7112E-08,3.4223E-08,-1.7112E-08,0,0,-1.225E-15,0,0,0,0,0,0,0,0,0,0, &
     & 0,-1.7112E-08,5.1337E-08,-1.7112E-08,0,0,-1.7113E-08,0,0,0,0,0,0,0,0,0,&
     & 0,0,-1.7112E-08,3.4225E-08,0,0,0,-1.7113E-08,0,0,0,0,0,0,0,0,&
     & -1.7113E-08,0,0,0,3.4228E-08,-1.225E-15,0,0,-1.7115E-08,0,0,0,0,0,0,0,&
     & 0,-1.225E-15,0,0,-1.225E-15,4.9E-15,-1.225E-15,0,0,-1.225E-15,0,0,0,0,0,0,&
     & 0,0,-1.7113E-08,0,0,-1.225E-15,5.1341E-08,-1.7113E-08,0,0,-1.7115E-08,0,0,0,0,0,&
     & 0,0,0,-1.7113E-08,0,0,-1.7113E-08,5.1341E-08,0,0,0,-1.7115E-08,0,0,0,0,&
     & 0,0,0,0,-1.7115E-08,0,0,0,5.1344E-08,-1.7114E-08,0,0,-1.7115E-08,0,0,0,&
     & 0,0,0,0,0,-1.225E-15,0,0,-1.7114E-08,5.1343E-08,-1.7114E-08,0,0,-1.7115E-08,0,0,&
     & 0,0,0,0,0,0,-1.7115E-08,0,0,-1.7114E-08,6.8457E-08,-1.7114E-08,0,0,-1.7115E-08,0,&
     & 0,0,0,0,0,0,0,-1.7115E-08,0,0,-1.7114E-08,5.1343E-08,0,0,0,-1.7115E-08,&
     & 0,0,0,0,0,0,0,0,-1.7115E-08,0,0,0,5.7048E-08,-2.2819E-08,0,0,&
     & 0,0,0,0,0,0,0,0,0,-1.7115E-08,0,0,-2.2819E-08,7.9867E-08,-2.2819E-08,0,&
     & 0,0,0,0,0,0,0,0,0,0,-1.7115E-08,0,0,-2.2819E-08,7.9866E-08,-2.2818E-08,&
     & 0,0,0,0,0,0,0,0,0,0,0,-1.7115E-08,0,0,-2.2818E-08,5.7047E-08/), (/N,N/))
  B = reshape((/2.538E-09, 2.538E-09, 2.538E-09, 2.538E-09, 2.538E-09, 2.538E-09,&
     & 2.538E-09, 2.538E-09, 2.538E-09, 2.538E-09, 2.538E-09, 2.538E-09, &
     & 2.538E-09, 2.538E-09, 2.538E-09, 2.538E-09/), (/16/))

  jcnt = 0
  do i=1, N
     ia(i) = jcnt + 1
     do j=i, N
        if (dabs(A(i,j)) > 1.e-20 .or. i==j) then
           jcnt = jcnt + 1
           ax(jcnt) = A(i,j)
           jx(jcnt) = j
        end if
     end do
  end do
  ia(N+1) = jcnt + 1

  allocate(ja(jcnt), aa(jcnt))
  ja(1:jcnt) = jx(1:jcnt)
  aa(1:jcnt) = ax(1:jcnt)
  deallocate(jx,ax)
  allocate(x(N), stat=ierr)

  NRHS = 1
  error = dss_create(handle, MKL_DSS_DEFAULTS)
  error = dss_define_structure( handle, MKL_DSS_SYMMETRIC, &
       &  ia, N, N,  ja, jcnt)
  error = dss_reorder( handle, MKL_DSS_DEFAULTS, idum)
  error = dss_factor_real( handle, MKL_DSS_DEFAULTS, aa)
  error = dss_solve_real( handle, MKL_DSS_DEFAULTS, B, nRhs,  x)
  error = dss_delete( handle, MKL_DSS_DEFAULTS )
  print *, x
  print *, matmul(A,x)
  deallocate(x, A, aa, ia, ja, B, stat=ierr)
end program using_dss
```

# Numpy code for converting CSR into dense matrix

```python
N = 8
jcnt = 18
isSYM = True
ia = [1,5,8,10,12,15,17,18,19]
ja = [1,3,6,7, 2,3,5,3,8,4,7,5, 6,7,6,8, 7,8]
A =  [7,1,2,7,-4,8,2,1,5,7,9,5,-1,5,0,5,11,5]

AA = np.zeros([N,N])
isSYM = False
N = 8
jcnt = 20
ia = [1,5,8,10,12,13,16,18,21]
ja = [1,3,6,7, 2,3,5,3,8,4,7, 2,3,6,8, 2, 7, 3,7,8]
A  = [7,1,2,7,-4,8,2,1,5,7,9,-4,7,3,5,17,11,-3,2,5]

i = 1
if (isSYM):
    for j in range (jcnt):
        y = ja[j] - 1
        if j+1 > (ia[i]-1):
            i += 1
        x = i-1
        AA[x][y] = A[j]
        AA[y][x] = A[j]
        print (x,y,A[j])
else:
    for j in range (jcnt):
        y = ja[j] - 1
        if j+1 > (ia[i]-1):
            i += 1
        x = i-1
        AA[x][y] = A[j]
        print (x,y,A[j])

plt.matshow(AA)
plt.show()
plt.matshow(AA[0:10,0:10])
plt.show()
```





