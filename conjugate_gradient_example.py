"""This formulation solves the model

    min_x ||Ax - b||_2^2

where A is the ray transform.
"""

from util import load_data
import odl

data = load_data()

space = odl.uniform_discr([-150, -150], [150, 150], [600, 600])
geometry = odl.tomo.parallel_beam_geometry(space,
                                           angles=data.shape[1],
                                           det_shape=data.shape[2])
ray_trafo = odl.tomo.RayTransform(space, geometry, impl='astra_cuda')

x = ray_trafo.domain.zero()
rhs = ray_trafo.range.element(data[1])
odl.solvers.conjugate_gradient_normal(ray_trafo, x, rhs, 100)

x.show('result')
