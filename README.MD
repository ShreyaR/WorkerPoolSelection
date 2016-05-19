Dependencies
-----------------------------
- boto
- gsl
- zmdp

Places to change paths
-----------------------------
- Ballots.py, line 43
- Ballots.py, line 55
- main.py, line 48
- main.py, line 51

Other Changes to Make
-----------------------------
- EM/MakeFile, path for GSLInclude
- Run MakeFile again

How to Run
-----------------------------
1. Make 'em' (from inside 'EM' folder)
2. Edit the path (for all the location listed under the 'Places to change paths' tab) to your current working directory.
3. If running in simulation, then run BallotGenerator.py to simulate workers and ballots, according to a given distribution. The ballots are then saved offline in SimulatedData. Else, run LiveBallotReader.py, and point the path in LiveBallotReader.py to the path where live experiment results are saved. Note: Always have the WorkerPool.info file in the simulated data, the scripts will do the rest.
4. RunSimulations.py (in the main directory) is a wrapper that lets you conduct all experiemnts in a centralised manner. You can run Live or Simulated Experiments from within the RunSimulations file. Can toggle with the number of repetiions the experiments must be run for.
5. Run RunSimulations.py to start running all the experiments. 
6. RunSimulations.py can be run in 2 modes. 
	-- 	Mode 0:
		Generates Simlation Parameters if not already generated.
	--	Mode 1:
		Runs ZMDP package for different worker pools + the combined model.
7. If running RunSimulations.py for LiveExperiments, then to get average costs and accuracies, run script.py that should be present in the respective directory for that set of results. 'script.py' will print the averages.