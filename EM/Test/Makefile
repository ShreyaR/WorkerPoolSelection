default: testNormalDraw

clean:
	rm -f *.o testNormalDraw

# Set these variables to the point to the correct locations

GSL_INCLUDE=/opt/local/include/

testNormalDraw: testNormalDraw.c
gcc-mp-4.8 -O3 -I $(GSL_INCLUDE) -L/opt/local/lib -std=c99 -o testNormalDraw -lm -lgsl -lgslcblas