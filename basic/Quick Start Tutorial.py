# import hoomd and the md package
from hoomd import *
from hoomd import md

# initialize the execution context
context.initialize('--mode=cpu')

# create a simple cubic lattice of 125 particles
system = init.create_lattice(unitcell=lattice.sc(a=2.0), n=5)

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
