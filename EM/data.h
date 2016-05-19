#ifndef DATA_H
#define DATA_H

#include <gsl/gsl_vector.h>

typedef struct {
  int imageIdx;
  int labelerId;
  int workflowId;
  int workerPoolId;
  int label;
  double trueLabel;
  double trueDifficulty;
} Label;

typedef struct {
  Label *labels;
  int numLabels;
  int numLabelers;
  int numImages;
  int numWorkflows;
  int numWorkerPools;
  double *priorAlpha;
  double *priorBeta;
  double *probZ1, *probZ0;
  double *alpha, *beta;
  double *priorZ1;
} Dataset;

void packX (gsl_vector *x, Dataset *data);
void unpackX (const gsl_vector *x, Dataset *data);
void readData (char *filename, Dataset *data, double*, double);
void outputResults (Dataset *data);

#endif
