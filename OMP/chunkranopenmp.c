/*DESICRIPTION:  
 *   OpenMp Example - Matrix Multiply - C Version
 *   Demonstrates a matrix multiply using OpenMP. Threads share row iterations
 *   according to a predefined chunk size.
 * AUTHOR: Blaise Barney
 * LAST REVISED: 06/28/05
 ******************************************************************************/
#include <omp.h>
#include <stdio.h>
#include <stdlib.h>

#define NRA 200                 /* number of rows in matrix A */
#define NCA 200                /* number of columns in matrix A */
#define NCB 200                 /* number of columns in matrix B */

int main (int argc, char *argv[]) 
{
	int	tid, nthreads, i, j, k, chunk, xyz;
	double	a[NRA][NCA],           /* matrix A to be multiplied */
		b[NCA][NCB],           /* matrix B to be multiplied */
		c[NRA][NCB];           /* result matrix C */
	omp_set_num_threads(atoi(argv[1]));
	unsigned int state[atoi(argv[1])];
	
	chunk = atoi(argv[2]);                    /* set loop iteration chunk size */

	/*** Spawn a parallel region explicitly scoping all variables ***/
#pragma omp parallel shared(a,b,c,nthreads,chunk) private(tid,i,j,k,xyz)
	{
		tid = omp_get_thread_num();
		if (tid == 0)
		{
			nthreads = omp_get_num_threads();
			printf("Starting matrix multiple example with %d threads\n",nthreads);
			//printf("Initializing matrices...\n");
		}
		/*** Initialize matrices ***/
#pragma omp for schedule (dynamic,chunk)
		for (i=0; i<NRA; i++)
			for (j=0; j<NCA; j++)
				a[i][j]= i+j;
#pragma omp for schedule (dynamic,chunk)
		for (i=0; i<NCA; i++)
			for (j=0; j<NCB; j++)
				b[i][j]= i*j;
#pragma omp for schedule (dynamic,chunk)
		for (i=0; i<NRA; i++)
			for (j=0; j<NCB; j++)
				c[i][j]= 0;

		/*** Do matrix multiply sharing iterations on outer loop ***/
		/*** Display who does which iterations for demonstration purposes ***/
		//printf("Thread %d starting matrix multiply...\n",tid);
#pragma omp for schedule (dynamic,chunk)
		for (i=0; i<NRA; i++)    
		{
			//printf("Thread=%d did row=%d\n",tid,i);
			for(j=0; j<NCB; j++)       
				for (k=0; k<NCA; k++){
					int xzy = rand_r((&state[tid])) + rand_r(&state[tid]) * rand_r(&state[tid]);
					//    c[i][j] += a[i][k] * b[k][j];
				}
		}
	}   /*** End of parallel region ***/

	/*** Print results ***/
	//printf("******************************************************\n");
	//printf("Result Matrix:\n");
	//for (i=0; i<NRA; i++)
	//{
	//for (j=0; j<NCB; j++) 
	//printf("%6.2f   ", c[i][j]);
	//printf("\n"); 
	//}
	//printf("******************************************************\n");
	//printf ("Done.\n");

}
