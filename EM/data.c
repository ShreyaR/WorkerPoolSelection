#include <math.h>
#include "data.h"

void packX (gsl_vector *x, Dataset *data)
{
	int i, j;

	/* Pack alpha and beta into gsl_vector */
	for (i = 0; i < data->numLabelers * data->numWorkflows; i++) {
		gsl_vector_set(x, i, data->alpha[i]);
	}
	for (j = 0; j < data->numImages * data->numWorkflows; j++) {
		gsl_vector_set(x, data->numLabelers * data->numWorkflows + j, 
			       data->beta[j]);
	}
}

void unpackX (const gsl_vector *x, Dataset *data)
{
	int i, j;

	/* Unpack alpha and beta from gsl_vector */
	for (i = 0; i < data->numLabelers * data->numWorkflows; i++) {
	  data->alpha[i] = gsl_vector_get(x, i);
		/*if (isnan(data->alpha[i])) {
			abort();
		}*/
	}
	for (j = 0; j < data->numImages * data->numWorkflows; j++) {
	  data->beta[j] = gsl_vector_get(x, 
					 (data->numLabelers * data->numWorkflows) + j);
		/*if (isnan(data->beta[j])) {
			abort();
		}*/
	}
}

/* read the data, and set the prior */
void readData (char *filename, Dataset *data, double *pa, double pb)
{
	int i, j;
	int idx;
	char str[1024];
	FILE *fp = fopen(filename, "rt");
	double priorZ1;

	/* Read parameters */
	fscanf(fp, "%d %d %d %d %d %lf\n", &data->numLabels, &data->numLabelers, &data->numImages, &data->numWorkflows, &data->numWorkerPools, &priorZ1);
	/*printf("Reading %d labels of %d labelers over %d images for prior P(Z=1) = %lf and %d worker pools.\n",
	       data->numLabels, data->numLabelers, data->numImages, priorZ1, data->numWorkerPools);*/

	data->priorAlpha = (double *) malloc(sizeof(double) * data->numLabelers * data->numWorkflows);

	/*printf("Assuming prior on alpha has mean 1 and std 1\n");*/
	/*for (i = 0; i < data->numLabelers * data->numWorkflows; i++) {
		data->priorAlpha[i] = pa;
	} */
	/*default value */

	data->priorBeta = (double *) malloc(sizeof(double) * data->numImages * data->numWorkflows);
	data->priorZ1 = (double *) malloc(sizeof(double) * data->numImages);

	///SCOPE FOR IMPROVEMENT: GIVE THE TRUTH VALUE THAT THE POMDP FIGURES OUT AS THE PRIOR FOR EACH IAMGE LABEL

	/*printf("Assuming prior on beta has mean 1 and std 1.\n");
	printf("Also assuming p(Z=1) is the same for all images.\n");*/
	for (j = 0; j < data->numImages * data->numWorkflows; j++) {
		data->priorBeta[j] = pb; /* default value */
	}
	for (j = 0; j < data->numImages; j++) {
		data->priorZ1[j] = priorZ1;
	}
	data->probZ1 = (double *) malloc(sizeof(double) * data->numImages);
	data->probZ0 = (double *) malloc(sizeof(double) * data->numImages);
	data->beta = (double *) malloc(sizeof(double) * data->numImages * data->numWorkflows);
	data->alpha = (double *) malloc(sizeof(double) * data->numLabelers * data->numWorkflows);
	data->labels = (Label *) malloc(sizeof(Label) * data->numLabels);

	int *tracker = (int *) malloc(sizeof(int) * data->numLabelers);
	for (int j = 0; j < data->numLabelers;j++){
	    tracker[j] = 0;
	}

    //printf("Am I here?\n");
	/* Read labels */
	idx = 0;
	while (fscanf(fp, "%d %d %d %d %d %lf\n", &(data->labels[idx].imageIdx),&(data->labels[idx].labelerId),
	                    &(data->labels[idx].workflowId),&(data->labels[idx].workerPoolId),
	                    &(data->labels[idx].label),&(data->labels[idx].trueLabel)) == 6) {
        //printf("%d\n",idx);
        /* How are workers indexed in data? Seems to be that the input file must contain workers from 0 to numLabelers-1*/
        if (tracker[data->labels[idx].labelerId] == 0){
		    data->priorAlpha[data->labels[idx].labelerId] = pa[data->labels[idx].workerPoolId];
		    tracker[data->labels[idx].labelerId] = 1;
		}
		data->priorZ1[data->labels[idx].imageIdx] = data->labels[idx].trueLabel;
		//data->priorBeta[data->labels[idx].imageIdx] = data->labels[idx].trueDifficulty;
		/*if (data->labels[idx].label != 0 && data->labels[idx].label != 1) {
			abort();
		}*/
		//printf("Read: image(%d)=%d by labeler %d in pool %d\n", data->labels[idx].imageIdx,
		//       data->labels[idx].label, data->labels[idx].labelerId, data->labels[idx].workerPoolId);
		idx++;
	}
	fclose(fp);
}

void outputResults (Dataset *data)
{
	int i, j;

	for (i = 0; i < data->numLabelers * data->numWorkflows; i++) {
//		printf("Alpha[%d] = %f\n", i, data->alpha[i]);
		printf("%f\n", data->alpha[i]);
	}
	for (j = 0; j < data->numImages * data->numWorkflows; j++) {
		printf("Beta[%d] = %f\n", j, data->beta[j] );
	}

	for (j = 0; j < data->numImages; j++) {
		printf("P(Z(%d)=1) = %f\n", j, data->probZ1[j]);
		printf("P(Z(%d)=0) = %f\n", j, data->probZ0[j]);
	}

}
