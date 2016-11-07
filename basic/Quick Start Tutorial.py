# import hoomd and the md package
from hoomd import *
from hoomd import md

# initialize the execution context
context.initialize('--mode=cpu')

# create a simple cubic lattice of 125 particles
system = init.create_lattice(unitcell=lattice.sc(a=2.0), n=5)
snap_0 = system.take_snapshot(all=True)

# specify Lennard-Jones interactions between particle pairs
nl = md.nlist.cell()
lj = md.pair.lj(r_cut=3.0, nlist=nl)
lj.pair_coeff.set('A', 'A', epsilon=1.0, sigma=1.0)

# integrate with brownian dynamics
all = group.all();
md.integrate.mode_standard(dt=0.001)
md.integrate.brownian(group=all, kT=0.1, seed=987)

# run 200,000 time steps
run(2e5)

# take a snapshot of the current state of the system and save the particle positions
snap_1 = system.take_snapshot(all=True)
pos_0 = snap_0.particles.position
pos_1 = snap_1.particles.position

# a visual representation using matplotlib
# import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

fig = plt.figure()
ax_0 = fig.add_subplot(121, projection='3d')
for part in pos_0:
    ax_0.scatter(part[0], part[1], part[2], c='y')

ax_1 = fig.add_subplot(122, projection='3d')
for part in pos_1:
    ax_1.scatter(part[0], part[1], part[2], c='y')

plt.show()
