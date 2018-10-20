# SlitherLinkACO

UWA CITS4404 Artifical Intelligence & Adaptive Systems Project. Using an ACO alogithm to solve Slitherlink logic puzzles.

## Running


To run the script with a puzzle simply type the following into the command line, with the filename being the puzzle to solve.
```
$ python main.py filename.txt
```
Files must be stored in the 'puzzles' directory as .txt files, with the required format. The first line must specify the row and column number seperated with a comma. Then each line after that represents a row, with the number of charcters in that line being the number of columns. These characters can either be an integer 0,1,2 or 3 indicating the required number of edges around that box. If there should be no number simply use a fullstop to indicate an empty box.

Here's an example of puzzle correctly formated below. See the 'puzzles' directory for more examples.
```
3,5
.3..3
.0.2.
.3..1
```

The script can also be run with several optional flags:
```
 -h, --help                                
    Displays the help guide with optional flags and meanings
 
-p, --pheromones                  
    Display relative pheromone distribution instead of best solution (Only displays when -t flag off)
  
-r,  --random                         
    Turns off the use of the heuristic with the ACO
  
-s, --startpoints                     
    The population of ants will be used for each starting point, and pheromones laid for each best ant from each starting point
  
-l,  --localized                        
    Uses a localised fitness function when laying pheromones for edges
  
-c, --cancel                            
    Cancels ant's route early if solution is known to be wrong
  
-d DYNAMIC, --dynamic DYNAMIC
    Fitness function weightings will adjust dynamically by increment of argument
  
-w [WEIGHTS [WEIGHTS ...]], --weights [WEIGHTS [WEIGHTS ...]]
    Fitness function weights as 3 floats representing; completeness, distance, single points, respectively (must not be more than 1 combined)
  
-t TESTING, --testing TESTING
    Takes a single argument, to run the ACO that number of times. Returns the user statistics of the results (will not display puzzle or any graphics)
  ```
