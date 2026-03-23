<p align="left">
  <img src="logo.png" alt="Package Logo" width="100" style="vertical-align: middle; margin-right: 10px;"/>
</p>

# multisoc
[![MAI_BIAS toolkit](https://img.shields.io/badge/MAI_BIAS-⚖️_AI_fairness_tool-white)](https://mammoth-eu.github.io/mammoth-commons/index.html)[![Integration tests](https://github.com/mammoth-eu/mammoth-commons/actions/workflows/integration.yml/badge.svg)](https://github.com/mammoth-eu/mammoth-commons/actions/workflows/integration.yml)
![Coverage](./coverage-badge.svg)
[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg)](code_of_conduct.md)
[![Downloads](https://static.pepy.tech/badge/mai-bias)](https://pepy.tech/projects/mai-bias)
[![PyPI](https://img.shields.io/pypi/v/hyperfair)](https://pypi.org/project/hyperfair/)
[![License](https://img.shields.io/github/license/CSHVienna/hyper_fair)](https://github.com/CSHVienna/hyper_fair/blob/main/LICENSE)

Multisoc is a Python package for simulating and analyzing networks with multidimensional interactions. Our multidimensional network model is based on aggregating latent connection preferences that depend on the attributes of the source node and the potential connection target. Although we have focused on evaluating aggregation mechanisms for these preferences, as a preliminary step, we need to consider how preferences may depend on attributes. 


The code also reproduces the results from the papers **A simple preference aggregation rule explains how multidimensional identities shape social networks** published in *Communication Physics* (available [here](https://www.nature.com/articles/s42005-026-02537-3)) and **Intersectional inequalities in social ties** published in *Science Advances* (available [here](https://www.science.org/doi/full/10.1126/sciadv.adu9025)).


This software is part of MAI-BIAS; a low-code toolkit for fairness analysis and mitigation, with an accompanying suite of coding tools. Our ecosystem operates in multidimensional, multi-attribute settings and across multiple data modalities (such as tabular data, images, text, and graphs). Learn more [**here**](https://mammoth-eu.github.io/mammoth-commons/index.html).

## 👥 Who is this for?
- **ML engineers and data scientists** building or evaluating network models in Python.
- **Researchers** studying multi-attribute connectivities in networks.
- **Policymakers and analysts** who want reproducible evidence for decision‑making. Consider exploring our user-friendly/no-code visualization tool to understand how multisoc works [**here**]([https://vis.csh.ac.at/ranks-of-disparity/index.html](https://vis.csh.ac.at/planets-of-disparity-two/)).

## ✨ About
**multisoc** is a principled theoretical framework to model multidimensional social interactions. Using Bayesian model selection, **multisoc** compares competing preference aggregation mechanisms in two empirical systems (high-school friendship networks and
marriages) and finds that a simple latent preference model outperforms more complex alternatives: people evaluate each identity dimension independently and form ties mainly when all evaluations are favorable. **multisoc** yields interpretable preference estimates and principled measures of dimension salience, providing a practical tool for analyzing social choices and identifying which aspects of identity matter most for tie formation. **multisoc** reveals how social structures emerge from intersecting identities, with broad implications for understanding social cohesion and addressing intersectional inequalities in networks.

## 🚀 Highlights
- ⚖️ Multivalue and multi-attribute network analyses

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
## No correlation would correspond to the group fraction of the largest minority (0.4 in this case)
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

In this example, we infer the one-dimensional preferences and the aggregation function, given a dummy dataset that contains three attributes: number, color and shape. After the code, you can see how the input data is structured.  
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

The `nodes_dummy.csv` file contains the information related to the nodes' attributes.  
Each row contains the index of the node, and the corresponding attributes.

|   index | shape   | color   |   number |
|--------:|:--------|:--------|---------:|
|       0 | Square  | Blue    |        3 |
|       1 | Circle  | Blue    |        3 |
|       2 | Square  | Red     |        5 |
|       3 | Square  | Blue    |        3 |
|       4 | Square  | Red     |        1 |


The `edges_dummy.csv` file contains the information related to the connection among the individuals.  
Each row contains one edge, with the corresponding source and target nodes.

|    |   source |   target |
|---:|---------:|---------:|
|  0 |        0 |        1 |
|  1 |        0 |       23 |
|  2 |        0 |       41 |
|  3 |        0 |       63 |
|  4 |        0 |      103 |

## 📜 Attributions
```bibtex
@article{martin2026simple,
  title={A simple preference aggregation rule explains how multidimensional identities shape social networks},
  author={Martin-Gutierrez, Samuel and Cartier van Dissel, Mauritz N and Karimi, Fariba},
  journal={Communications Physics},
  year={2026},
  publisher={Nature Publishing Group UK London}
}
@article{martin2025intersectional,
  title={Intersectional inequalities in social ties},
  author={Martin-Gutierrez, Samuel and Cartier van Dissel, Mauritz N and Karimi, Fariba},
  journal={Science Advances},
  volume={11},
  number={45},
  pages={eadu9025},
  year={2025},
  publisher={American Association for the Advancement of Science}
}
```
- **Project:** [MAMMOth](https://mammoth-ai.eu/)
- **Maintainer:** Samuel Martin-Gutierrez (martin.gutierrez.samuel@gmail.com)
- **License:** Apache 2.0
- **Contributors:** Mauritz Cartier van Dissel
