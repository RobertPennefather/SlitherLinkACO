# SlitherLinkACO

UWA CITS4404 Artifical Intelligence & Adaptive Systems Project. Using an ACO alogithm to solve slitherlink logic puzzles, first published by Nikoli in Japan.

## Running


To run the code with a puzzle simply type the following into the command line, with the filename being the puzzle to solve.
```
$ python main.py filename.txt
```

The code can also be run with several optional flags:
```
 -h, --help                                
 show this help message and exit
 
-p, --pheromones                  
  display pheromones instead of best solution (-t flag must be off)
  
-r,  --random                         
  flag turns off the use of the heuristic with the ACO
  
-s, --startpoints                     
  flag turns on getting every starting points best solution per iteration
  
-l,  --localized                        
  flag turns on using a localised fitness function for edge pheromones
  
-c, --cancel                            
  flag turns on the early cancel if ACO is known to be wrong
  
-d DYNAMIC, --dynamic DYNAMIC
    fitness weightings will adjust dynamically by increment of arg
  
-w [WEIGHTS [WEIGHTS ...]], --weights [WEIGHTS [WEIGHTS ...]]
  3 floats representing fitness weighting for; completeness, distance, single points, respectively (must not be more than 1 combined)
  
-t TESTING, --testing TESTING
  single argument, number of times to test ACO with puzzle
  ```
