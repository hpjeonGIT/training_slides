## Sample code for PI calculation
- MPI version
	- Ref: https://www.tankonyvtar.hu/hu/tartalom/tamop412A/2011-0063_23_introduction_mpi/ar01s04.html
    ```c
    #include <cstdlib>
    #include <ctime>
    #include <iostream>
    #include <math.h>
    #include <mpi.h>
    using namespace std;
    int main(int argc, char **argv){
      int id, nproc;
      MPI_Status status;
      double x,y, Pi, error;
      long long allsum;
      const long long iternum=1000000000;
      MPI_Init(&argc, &argv);
      MPI_Comm_rank(MPI_COMM_WORLD, &id);
      MPI_Comm_size(MPI_COMM_WORLD, &nproc);
      srand((unsigned)time(0));
      cout.precision(12);
      long long sum=0;
      for(long long i=0;i<iternum;++i){
        x=(double)rand()/RAND_MAX;
        y=(double)rand()/RAND_MAX;
        if(x*x+y*y<1) ++sum;
      }
      //Slave:
      if(id!=0){
        MPI_Send(&sum, 1, MPI_LONG_LONG, 0, 1, MPI_COMM_WORLD);
      }
      //Master:
      else{
        allsum=sum;
        for(int i=1;i<nproc;++i){
          MPI_Recv(&sum, 1, MPI_LONG_LONG, MPI_ANY_SOURCE, 1, MPI_COMM_WORLD,
               &status);
          allsum+=sum;
        }
        //calculate Pi, compare to the Pi in math.h
        Pi=(4.0*allsum)/(iternum*nproc);
        error = fabs( Pi-M_PI );
        cout<<"Pi: \t\t"<<M_PI<<endl;
        cout<<"Pi by MC: \t"<<Pi<<endl;
        cout<<"Error: \t\t"<<fixed<<error<<endl;
      }
      // Terminate MPI:
      MPI_Finalize();
      return 0;
    }
    ```
	- Compile as `mpicxx mpi_version.c`
	- Run as `mpirun -n 4 ./a.out`
- A single GPU version
	- Ref: http://web.mit.edu/pocky/www/cudaworkshop/MonteCarlo/Pi.cu
    ```c
    // Written by Barry Wilkinson, UNC-Charlotte. Pi.cu  December 22, 2010.
    //Derived somewhat from code developed by Patrick Rogers, UNC-C
    #include <stdlib.h>
    #include <stdio.h>
    #include <cuda.h>
    #include <math.h>
    #include <time.h>
    #include <curand_kernel.h>
    #define TRIALS_PER_THREAD 4096
    #define BLOCKS 256
    #define THREADS 256
    #define PI 3.1415926535  // known value of pi
    __global__ void gpu_monte_carlo(float *estimate, curandState *states) {
        unsigned int tid = threadIdx.x + blockDim.x * blockIdx.x;
        int points_in_circle = 0;
        float x, y;
        curand_init(1234, tid, 0, &states[tid]);  
        // 	Initialize CURAND
        for(int i = 0; i < TRIALS_PER_THREAD; i++) {
            x = curand_uniform (&states[tid]);
            y = curand_uniform (&states[tid]);
            points_in_circle += (x*x + y*y <= 1.0f); 
            // count if x & y is in the circle.
        }
        estimate[tid] = 4.0f * points_in_circle / (float) TRIALS_PER_THREAD; 
        // return estimate of pi
    }
    int main (int argc, char *argv[]) {
        clock_t start, stop;
        float host[BLOCKS * THREADS];
        float *dev;
        curandState *devStates;
        printf("# of trials per thread = %d, # of blocks = %d, # of threads/block = %d.\n", TRIALS_PER_THREAD,
    BLOCKS, THREADS);
        start = clock();
        cudaMalloc((void **) &dev, BLOCKS * THREADS * sizeof(float)); 
        // allocate device mem. for counts
        cudaMalloc( (void **)&devStates, THREADS * BLOCKS * sizeof(curandState) );
        gpu_monte_carlo<<<BLOCKS, THREADS>>>(dev, devStates);
        cudaMemcpy(host, dev, BLOCKS * THREADS * sizeof(float), 
                   cudaMemcpyDeviceToHost); 
        // return results 
        float pi_gpu;
        for(int i = 0; i < BLOCKS * THREADS; i++) {
            pi_gpu += host[i];
        }
        pi_gpu /= (BLOCKS * THREADS);
        stop = clock();
        printf("GPU pi calculated in %f s.\n", (stop-start)/(float)CLOCKS_PER_SEC);
        printf("CUDA estimate of PI = %f [error of %f]\n", pi_gpu, pi_gpu - PI);
        return 0;
    }
    ```
	- Compile as `nvcc gpu.cu`
	- Run as `./a.out`
- MPI+GPU version
	- Ref: http://cacs.usc.edu/education/cs596/07-1MPI+OMP+CUDA.pdf
    ```c
    #include <stdio.h>
    #include <mpi.h>
    #include <cuda.h>
    #define NBIN 10000000 // Number of bins
    #define NUM_BLOCK 13 // Number of thread blocks
    #define NUM_THREAD 192 // Number of threads per block
    // Kernel that executes on the CUDA device
    __global__ void cal_pi(float *sum,int nbin,float step,float offset,
                           int nthreads,int nblocks)
    {
      int i;
      float x;
      int idx = blockIdx.x*blockDim.x+threadIdx.x; 
      // Sequential thread index across blocks
      for (i=idx; i< nbin; i+=nthreads*nblocks) { 
        // Interleaved bin assignment to threads
        x = offset+(i+0.5)*step;
        sum[idx] += 4.0/(1.0+x*x);
      }
    }
    int main(int argc,char **argv) {
      int myid,nproc,nbin,tid;
      float step,offset,pi=0.0,pig;
      dim3 dimGrid(NUM_BLOCK,1,1); // Grid dimensions (only use 1D)
      dim3 dimBlock(NUM_THREAD,1,1); // Block dimensions (only use 1D)
      float *sumHost,*sumDev; // Pointers to host & device arrays
      MPI_Init(&argc,&argv);
      MPI_Comm_rank(MPI_COMM_WORLD,&myid); // My MPI rank
      MPI_Comm_size(MPI_COMM_WORLD,&nproc); // Number of MPI processes
      nbin = NBIN/nproc; // Number of bins per MPI process
      step = 1.0/(float)(nbin*nproc); // Step size with redefined number of bins
      offset = myid*step*nbin; // Quadrature-point offset
      size_t size = NUM_BLOCK*NUM_THREAD*sizeof(float); //Array memory size
      sumHost = (float *)malloc(size); // Allocate array on host
      cudaMalloc((void **) &sumDev,size); // Allocate array on device
      cudaMemset(sumDev,0,size); // Reset array in device to 0
      // Calculate on device (call CUDA kernel)
      cal_pi <<<dimGrid,dimBlock>>> (sumDev,nbin,step,offset,NUM_THREAD,NUM_BLOCK);
      // Retrieve result from device and store it in host array
      cudaMemcpy(sumHost,sumDev,size,cudaMemcpyDeviceToHost);
      // Reduction over CUDA threads
      for(tid=0; tid<NUM_THREAD*NUM_BLOCK; tid++) pi += sumHost[tid];
      pi *= step;
      // CUDA cleanup
      free(sumHost);
      cudaFree(sumDev);
      printf("myid = %d: partial pi = %f\n",myid,pi);
      // Reduction over MPI processes
      MPI_Allreduce(&pi,&pig,1,MPI_FLOAT,MPI_SUM,MPI_COMM_WORLD);
      if (myid==0) printf("PI = %f\n",pig);
      MPI_Finalize();
      return 0;
    }
    ```
	- Compile as `nvcc -Xcompiler -fopenmp hypi.cu -I/share/ompi/401_gcc74_cuda_ucx151/include -L/share/ompi/401_gcc74_cuda_ucx151/lib -lmpi -lgomp`
	- Run as `export CUDA_VISIBLE_DEVICES=0,1; mpirun -n 2 ./a.out`

