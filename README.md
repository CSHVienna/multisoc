# multisoc

multisoc is a python package to simulate and analyze networks with multidimensional interactions. 

The code also reproduces the results from our paper on multidimensional social interactions. Preprint available at https://arxiv.org/abs/2406.17043.


## Example

In this example, we generate a graph using the `multidimensional_network_fix_av_degree` function
```python
import numpy as np
from multisoc.generate.multidimensional_network import multidimensional_network_fix_av_degree
from multisoc.generate.two_dimensional_population import consol_comp_pop_frac_tnsr

## List of 1d homophily matrices (2 for a two-dimensional system)
h_mtrx_lst = [ 
    np.array([[0.9,0.1],
              [0.1,0.9]]),
    np.array([[0.6,0.4],
              [0.4,0.6]])
]

## The marginals of the population distribution defined by comp_pop_frac_tnsr
## Each row has to sum 1 (100% of the population)
pop_fracs_lst = [
    [0.2,0.8],
    [0.4,0.6]
]

## Generate population distribution with certain level of correlation between the two attributes
## No correlation would correspond to the fraction of the largest minority
consol = 0.4 ## Level of correlation
comp_pop_frac_tnsr = consol_comp_pop_frac_tnsr(pop_fracs_lst,consol)

N = 200 ## Number of nodes
m = 20  ## Average number of connections per node

kind = "all" ## Aggregation function: {all->and, one->mean, any->or}
p_d = [0.5, 0.5] ## Weight of each dimension for "mean" aggregation function

G = multidimensional_network_fix_av_degree(
                h_mtrx_lst,
                comp_pop_frac_tnsr,
                kind,
                directed=False, ## Directed or undirected network
                pop_fracs_lst = pop_fracs_lst,
                N=N,
                m=m,
                v = 0,
                p_d = p_d
                )
```


## Install

Install the latest version
```python
pip install multisoc
```