#!/usr/bin/env python
"""
The example is an extension of robot_discrete_simple.py by including
disturbance and input computation using the "closed loop" algorithm.

Petter Nilsson (pettni@kth.se)
August 14, 2011

NO, system and cont. prop definitions based on TuLiP 1.x
2 Jul, 2013
NO, TuLiP 1.x discretization
17 Jul, 2013
"""

import sys, os
import numpy as np

from tulip import *
import tulip.polytope as pc
from tulip.abstract import prop2part, discretize

# Problem parameters
input_bound = 1.0
uncertainty = 0.01

# Continuous state space
cont_state_space = pc.Polytope.from_box(np.array([[0., 2.],[0., 3.]]))


# Continuous dynamics
A = np.array([[1.0, 0.],[ 0., 1.0]])
B = np.array([[0.1, 0.],[ 0., 0.1]])
E = np.array([[1,0],[0,1]])
U = pc.Polytope.from_box(input_bound*np.array([[-1., 1.],[-1., 1.]]))
W = pc.Polytope.from_box(uncertainty*np.array([[-1., 1.],[-1., 1.]]))

sys_dyn = hybrid.LtiSysDyn(A,B,E,[],U,W, cont_state_space)


# Continuous proposition
cont_props = {}
cont_props['X1'] = pc.Polytope.from_box(np.array([[0., 1.],[0., 1.]]))
cont_props['X2'] = pc.Polytope.from_box(np.array([[1., 2.],[2., 3.]]))

# Compute the proposition preserving partition of the continuous state space
cont_partition = prop2part.prop2part(cont_state_space, cont_props)
disc_dynamics = discretize.discretize(cont_partition, sys_dyn, closed_loop=True, \
                N=8, min_cell_volume=0.1, verbose=0)

# TEST (to be removed):
# import networkx as nx
# from tulip.polytope.plot import plot_partition
# plot_partition(disc_dynamics.ppp, np.array(nx.to_numpy_matrix(disc_dynamics.ofts)))
# print disc_dynamics.ofts
# end of TEST

# TO DO (when the relevant pieces are in place):
# Specifications
# Discretization
# Synthesis
# Simulation
