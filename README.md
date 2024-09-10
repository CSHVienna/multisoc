# multisoc

multisoc is a python package to simulate and analyze networks with multidimensional interactions. 

The code also reproduces the results from the paper ***The hidden architecture of connections: How do multidimensional identities shape our social networks?***.  
Preprint available at https://arxiv.org/abs/2406.17043.

## Installation

Install the latest version:
```
pip install multisoc
```

Install from source:
```
git clone https://github.com/CSHVienna/multisoc
cd multisoc
pip install -e .
```

## Examples

### Multidimensional graph generation
In this example, we generate a graph, with two attributes and two categories per attribute, using the `multidimensional_network_fix_av_degree` function.  
The graph is very homophilic in the first attribute, and slightly homophilic in the second one.
Furthermore, the population distributions of the two attributes are slightly correlated.

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

### Inference of multidimensional interactions 

In this example, we infer the one-dimensional preferences and the aggregation function, given a dummy dataset that contains three attributes: number, color and shape.  
In particular, we print the value of AIC for the model that uses the AND aggregation function.

```python
from multisoc.infer import data_loader
from multisoc.infer import wrappers
import pandas as pd

# Load the data
nodes_dummy = pd.read_csv("./dummy_data/nodes_dummy.csv",index_col="index",dtype='category')
edges_dummy = pd.read_csv("./dummy_data/edges_dummy.csv",dtype='category')

# Describe the type of data 
dimensions_list = ['number','color','shape']
shape_list = ["Circle","Square"]
color_list = ["Blue","Red"]
number_list = ["1","2","3","4","5","6"]
all_attributes_dict = {
    "shape":shape_list,
    "color":color_list,
    "number":number_list
}

# Compute the result dictionary, if we suppose that the data was generated using the AND aggregation function
nodes_input, edges_input = data_loader.build_nodes_edges_input_df(nodes_dummy, edges_dummy, dimensions=["shape","color","number"])
results_1d_dct = wrappers.infer_latent_preferences_1dSimple(
    nodes_input,
    edges_input,
    dimensions_list, 
    all_attributes_dict,
    type_p = "and" ## Type of aggregation function {and,or,mean}
    )

# Print the AIC
print(results_1d_dct['AIC'])
```