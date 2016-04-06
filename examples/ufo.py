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

from omgtools import *

# create fleet
N = 3
vehicles = [Quadrotor(0.2) for l in range(N)]

fleet = Fleet(vehicles)
configuration = RegularPolyhedron(0.6, N, -np.pi/2).vertices.T
init_positions = [-1., -1.] + configuration
terminal_positions = [11., 11.] + configuration

fleet.set_configuration(configuration.tolist())
fleet.set_initial_conditions(init_positions.tolist())
fleet.set_terminal_conditions(terminal_positions.tolist())

# create environment
environment = Environment(room={'shape': Square(14.), 'position': [5., 5.]})
trajectory = {'velocity': {1.: [-9, 0.]}}
environment.add_obstacle(
    Obstacle({'position': [13, 4.]}, UFO(1.5, 0.6), trajectory))

# create a formation point-to-point problem
options = {'horizon_time': 5., 'codegen': {
    'jit': False}, 'admm': {'rho': 0.07}}
problem = FormationPoint2point(fleet, environment, options=options)
# problem.set_options({'solver': {'linear_solver': 'ma57'}})
problem.init()

# create simulator
simulator = Simulator(problem)
simulator.plot.set_options({'knots': True})
simulator.plot.show('scene')

# run it!
simulator.run()

# show/save some results
simulator.plot.show_movie('scene', repeat=False)
