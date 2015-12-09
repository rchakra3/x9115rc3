## Code8: Comparison of Simulated Annealing, Differential Evolution and MaxWalkSat to optimze DTLZ7

### Abstract

This experiment attempts to compare the performance of Differential Evolution, Max-WalkSat and Simulated Annealing by running them on the DTLZ7 model with 10 decision variables and 2 objective functions.

### Introduction

#### Simulated annealing
Simulated annealing is an optimization technique with very little overhead ( it only maintains the state of 3 different candidates at any point in time), but also often has difficulty performing as well as other optimization techniques. It works by making random jumps across the decision space and comparing to the current solution as well as the best solution seen thus far. With a probability that decreases with an increase in iterations, Simulated Annealing jumps to sub-optimal solutions. The idea behind this is that moving to a locally sub optimal solutions in the first few iterations might enable moving towards a globally optimal solution in later iterations.

#### Max-WalkSat
Max-WalkSat is a stochastic method for sampling the landscape of the local region. The main idea behind it is that in large search landscapes, good solutions are in very small areas. Thus, it tries to make progress by moving around the local search landscape and if it doesn't make much improvement in this local area, it jumps to another region in the search landscape. Thus, it tends to perform better than simulated annealing in terms of quality of solutions, which does not take advantage of the search landscape at all.


#### Differential Evolution

DE optimizes a problem by maintaining a population of candidate solutions and creating new candidate solutions by combining existing ones according to a formula which depends on the variation of DE being used, and then keeping whichever candidate solution has the best score or fitness on the optimization problem at hand. Such methods are commonly known as metaheuristics as they make few or no assumptions about the problem being optimized and can search very large spaces of candidate solutions. However, metaheuristics such as DE do not guarantee an optimal solution is ever found.

In this experiment, I have used DE/rand/1:
   - Extrapolate from some candidate X, chosen at random.
   - Add in values from one other extrapolation (Y-Z)


### Scott-knott

The Scott & Knott method make use of a cluster analysis algorithm, where, starting from the whole group of observed mean effects, it divides, and keep dividing the sub-groups in such a way that the intersection of any two groups formed in that manner is empty [3]

### DTLZ7

DTLZ7 is one of the models in the DTLZ class of models, which were designed to stress test optimizers. In this particular experiment I have used DTLZ7 with 10 decision variables and 2 objective functions. In later experiments, the DTLZ model as well as the number of variables and objective functions has been varied.

### Expected Results

Simulated Annealing is an extremely simple optimization technique that tries to find better solutions simply with random jumps. There is no local optimization as in Max-Walksat, nor is there an effort to combine known "good" solutions at each stage.

Max-Walksat on the other hand, makes random jumps but tries to optimize locally after each such random jump. Thus, it tends to at least move towards a locally optimal solution.

Differential Evolution on the other hand, is a much more intensive algorithm. It maintains a frontier or list of candidates of size `frontier_size` and then tries to incrementally improve on them by combining them into new candidate solutions. These new candidate solutions are checked against the original candidates and if they are better, the original candidates are replaced. In this way, we avoid over population and try to move towards better solutions.

Since DE is a much more informed and intensive algorithm which maintains a list of the best candidates over multiple iterations, it is expected that DE should perform better than Max-Walksat. Max-Walksat in turn should perform better than Simulated annealing since at the very least, it attempts to optimize locally.


### Implementation and results
In this experiment, I have evaluated three optimizers:
1. Simulated annealing
2. Max-Walksat
3. Differential Evolution

In order to do this I've used three comparators:

- Type 1 comparator:
   Used to compare any two candidate solutions. I have used simple aggregation of objective function values for this, since for DTLZ 7 the objectives are not "combative"


- Type 2 comparator
   - Used to compare eras of the same optimzer. I have used A12 for this and used 0.56 as the cutoff value. This basically means that there is improvement if the values of the objectives in the new era are better at least 56% of the time.
   - If there is no improvement, number of lives is decreased by 1
   - If there is improvement, number of lives is increased by 5

Early Termination Counts:

| Optimizer | Number of  early terminations  |
|-----------|--------------------------------|
| DE        | 6                              |
| SA        | 5                              |
| MWS       | 0                              |



- Type 3 comparator
   Used to compare the final eras between multiple optimizers (DE, MWS and SA in this case).

Method used:
   - Repeat 20 times:
      - For DTLZ7 with 10 decision variables and 2 objective functions. generate an initial population:
         - Run SA
         - Run MWS
         - Run DE
   - Plot the output using SK charts as shown below:

Output:
```
rank ,         name ,    med   ,  iqr 
----------------------------------------------------
   1 ,         de19 ,    8.11  ,  1.40 (    --*        |              ), 7.49,  8.12,  8.89
   1 ,         de18 ,    8.21  ,  1.25 (    --*        |              ), 7.58,  8.21,  8.83
   1 ,         de17 ,    8.22  ,  1.42 (    --*-       |              ), 7.61,  8.22,  9.04
   1 ,          de4 ,    8.25  ,  1.26 (     -*-       |              ), 7.71,  8.28,  8.97
   1 ,          de8 ,    8.28  ,  1.15 (     -*-       |              ), 7.79,  8.29,  8.95
   1 ,         de16 ,    8.29  ,  1.35 (     -*-       |              ), 7.69,  8.29,  9.04
   1 ,         de10 ,    8.34  ,  1.16 (     -*-       |              ), 7.78,  8.34,  8.95
   1 ,         de13 ,    8.35  ,  1.39 (     -*-       |              ), 7.76,  8.36,  9.15
   2 ,          de2 ,    8.38  ,  1.14 (     -*-       |              ), 7.81,  8.39,  8.94
   2 ,          de9 ,    8.39  ,  1.19 (     -*-       |              ), 7.78,  8.40,  8.97
   2 ,          de1 ,    8.42  ,  1.32 (     -*-       |              ), 7.79,  8.43,  9.11
   2 ,          de3 ,    8.45  ,  1.25 (     -*-       |              ), 7.82,  8.48,  9.07
   2 ,          de6 ,    8.48  ,  1.31 (     -*-       |              ), 7.97,  8.50,  9.28
   2 ,         de11 ,    8.48  ,  1.19 (     -*-       |              ), 8.00,  8.49,  9.18
   2 ,          de7 ,    8.48  ,  1.33 (     -*-       |              ), 7.82,  8.49,  9.16
   2 ,          de0 ,    8.50  ,  1.19 (     -*-       |              ), 7.91,  8.51,  9.10
   2 ,         de12 ,    8.58  ,  1.36 (     --*       |              ), 7.94,  8.59,  9.30
   2 ,         de15 ,    8.60  ,  1.29 (     --*       |              ), 7.80,  8.61,  9.10
   2 ,         de14 ,    8.62  ,  1.27 (     --*       |              ), 7.95,  8.62,  9.22
   2 ,          de5 ,    8.65  ,  1.11 (     --*       |              ), 8.05,  8.65,  9.16
   3 ,         mws7 ,    10.64  ,  2.68 (         ---*--|              ), 9.72,  10.66,  12.40
   3 ,         mws1 ,    10.65  ,  2.72 (         ---*--|              ), 9.52,  10.67,  12.25
   3 ,        mws15 ,    10.65  ,  2.71 (         ---*--|              ), 9.42,  10.65,  12.14
   4 ,        mws17 ,    10.96  ,  3.55 (         ---*--|-             ), 9.54,  10.96,  13.09
   4 ,         mws0 ,    10.96  ,  2.85 (         ---*--|              ), 9.54,  10.99,  12.39
   4 ,        mws13 ,    11.03  ,  2.61 (          ---*-|              ), 9.78,  11.10,  12.38
   4 ,         mws9 ,    11.17  ,  2.04 (          ---*-|              ), 10.17,  11.19,  12.21
   4 ,        mws14 ,    11.18  ,  2.26 (           --*-|              ), 10.34,  11.19,  12.60
   4 ,        mws18 ,    11.23  ,  2.45 (          ---*-|              ), 9.79,  11.23,  12.24
   4 ,         mws6 ,    11.37  ,  2.21 (          ---*-|              ), 10.07,  11.42,  12.29
   4 ,         mws3 ,    11.39  ,  2.26 (          ---*-|              ), 10.01,  11.41,  12.27
   5 ,         mws8 ,    11.54  ,  2.43 (           ---*|-             ), 10.53,  11.56,  12.97
   5 ,        mws10 ,    11.58  ,  2.70 (           ---*|-             ), 10.21,  11.59,  12.91
   5 ,         mws4 ,    11.60  ,  2.79 (          ----*|              ), 9.84,  11.66,  12.63
   5 ,        mws16 ,    11.71  ,  2.30 (            --*|-             ), 10.64,  11.73,  12.94
   5 ,        mws12 ,    11.72  ,  3.70 (          ----*|---           ), 10.03,  11.73,  13.73
   5 ,         mws2 ,    11.84  ,  2.48 (           ---*|-             ), 10.46,  11.85,  12.94
   5 ,         mws5 ,    11.96  ,  2.75 (           ----*-             ), 10.36,  12.00,  13.11
   6 ,        mws19 ,    11.98  ,  2.25 (             --*--            ), 11.11,  11.99,  13.36
   6 ,        mws11 ,    12.03  ,  1.95 (             --*-             ), 11.08,  12.05,  13.03
   7 ,         sa16 ,    12.62  ,  1.84 (              -|*-            ), 11.68,  12.63,  13.52
   7 ,         sa12 ,    12.76  ,  1.94 (              -|-*-           ), 11.75,  12.76,  13.70
   7 ,          sa0 ,    12.78  ,  2.39 (               |-*--          ), 11.88,  12.80,  14.27
   7 ,         sa14 ,    12.81  ,  2.11 (              -|-*-           ), 11.73,  12.81,  13.85
   7 ,          sa5 ,    12.81  ,  2.14 (              -|-*--          ), 11.85,  12.84,  13.99
   7 ,          sa2 ,    12.87  ,  2.02 (               |-*--          ), 12.02,  12.91,  14.04
   7 ,         sa11 ,    12.93  ,  1.98 (               |-*-           ), 11.95,  12.95,  13.92
   7 ,          sa1 ,    12.98  ,  2.15 (              -|-*-           ), 11.68,  12.99,  13.82
   7 ,         sa13 ,    13.00  ,  2.18 (              -|-*--          ), 11.77,  13.01,  13.96
   7 ,         sa10 ,    13.02  ,  1.85 (               |-*--          ), 12.19,  13.03,  14.04
   7 ,          sa9 ,    13.02  ,  2.31 (               |-*--          ), 11.91,  13.02,  14.22
   7 ,         sa17 ,    13.05  ,  2.23 (              -|-*--          ), 11.72,  13.07,  13.96
   7 ,         sa15 ,    13.06  ,  2.40 (               |-*--          ), 11.96,  13.08,  14.36
   7 ,          sa6 ,    13.06  ,  2.08 (               |-*--          ), 11.93,  13.07,  14.01
   7 ,         sa19 ,    13.08  ,  2.55 (              -|-*--          ), 11.71,  13.09,  14.27
   7 ,         sa18 ,    13.10  ,  2.27 (              -|--*-          ), 11.86,  13.15,  14.13
   7 ,          sa3 ,    13.13  ,  2.29 (              -|--*-          ), 11.82,  13.13,  14.11
   8 ,          sa8 ,    13.15  ,  2.53 (               |--*--         ), 12.12,  13.16,  14.65
   8 ,          sa4 ,    13.23  ,  2.16 (               |--*--         ), 12.25,  13.24,  14.41
   8 ,          sa7 ,    13.30  ,  1.96 (               |--*-          ), 12.09,  13.31,  14.05

```


### Threats to Validity

I have used a very simple Type1 operator which may not be very accurate. I can possibly improve on this by using a method such as continuous domination which tends to work better for a larger number of objectives

### Future Work

I have currently only run these models on DTLZ7 with 10 decision variables and 2 objective functions. It would be interesting to see the performance of these optimizers on other models and variations of the DTLZ models.

### Conclusion
Despite starting from the same initial populations, it is quite clear that Differential Evolution outperforms Max-Walksat and Simulated Annealing, and that Max-Walksat consistently outperforms Simulated Annealing. Furthermore, Differential Evolution consistently has results in a smaller range than the other two. These results seem consistent with initial expectations. 

### References

[1] https://cran.r-project.org/web/packages/ScottKnott/ScottKnott.pdf