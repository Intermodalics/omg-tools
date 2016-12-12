# This file is part of OMG-tools.
#
# OMG-tools -- Optimal Motion Generation-tools
# Copyright (C) 2016 Ruben Van Parys & Tim Mercy, KU Leuven.
# All rights reserved.
#
# OMG-tools is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 3 of the License, or (at your option) any later version.
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA
import os, sys
sys.path.insert(0, os.getcwd()+'/..')
from omgtools import *
import csv

# create vehicle
options = {'room_constraint': None, 'substitution': False}
vehicle = Dubins(bounds={'vmax': 0.7, 'wmax': np.pi/3., 'wmin': -np.pi/3.},
         		 options=options)
vehicle.define_knots(knot_intervals=5)  # choose lower amount of knot intervals
vehicle.set_initial_conditions([0.5, 0.5, 0.3])
vehicle.set_terminal_conditions([3.5, 3.5, 0.0])

# create environment
environment = Environment(room={'shape': Square(5.), 'position': [1.5, 1.5]})
rectangle = Rectangle(width=3., height=0.2)

environment.add_obstacle(Obstacle({'position': [-0.6, 1.0]}, shape=rectangle))
environment.add_obstacle(Obstacle({'position': [3.2, 1.0]}, shape=rectangle))

# create a point-to-point problem
options={'hard_term_con': True}
problem = Point2point(vehicle, environment, options, freeT=False)
problem.set_options({'solver_options': {'ipopt': {'ipopt.linear_solver': 'ma57'}}})
problem.init()

options = {}
casadi_path = os.path.join(os.getenv('HOME'), 'casadi-py27-np1.9.1-v3.1.0-rc1')
options['directory'] = os.path.join(os.getcwd(), 'export/')
# path to object files of your exported optimization problem
options['casadiobj'] = os.path.join(options['directory'], 'bin/')
# your casadi include path
options['casadiinc'] = os.path.join(casadi_path, 'include/')
# your casadi library path
options['casadilib'] = os.path.join(casadi_path, 'casadi/')
# specify source files
options['sourcefiles'] = ' '.join(['testDubins_p2p.cpp', 'Dubins_p2p.cpp'])

# export the problem
problem.export(options)
simulator = Simulator(problem)
# problem.plot('scene')
trajectories, signals = simulator.run()

# save results for check in c++
testdir = os.path.join(options['directory'], 'test')
if not os.path.isdir(testdir):
    os.makedirs(os.path.join(options['directory'], 'test'))
with open(os.path.join(testdir, 'data_state.csv'), 'wb') as f:
    w = csv.writer(f)
    for i in range(0, len(trajectories['state']), int(simulator.update_time/simulator.sample_time)):
        for k in range(trajectories['state'][i].shape[0]):
            w.writerow(trajectories['state'][i][k, :])
with open(os.path.join(testdir, 'data_input.csv'), 'wb') as f:
    w = csv.writer(f)
    for i in range(0, len(trajectories['input']), int(simulator.update_time/simulator.sample_time)):
        for k in range(trajectories['input'][i].shape[0]):
            w.writerow(trajectories['input'][i][k, :])

# note: you need to implement your vehicle type in c++. Take a look at
# Holonomic.cpp and Holonomic.hpp which are also exported as an example.