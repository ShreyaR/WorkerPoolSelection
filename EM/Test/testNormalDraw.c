#include <gsl/gsl_sf_erf.h>
#include <gsl/gsl_vector.h>
#include <math.h>
#include <time.h>
#include <stdio.h>
#include <stdlib.h>
//#include <gsl/gsl_ran_gaussian.h>

int main (int argc, char *argv[]){

    double a = gsl_sf_erf(1);
    printf("The random number we get is %f.", a);
    exit(0);
}