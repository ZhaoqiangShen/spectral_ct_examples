"""Example of Filtered-back projection reconstruction using ODL."""

import odl
from util import load_data

data = load_data()

space = odl.uniform_discr([-150, -150], [150, 150], [600, 600])

geometry = odl.tomo.parallel_beam_geometry(space,
                                           angles=data.shape[1],
                                           det_shape=data.shape[2])
ray_trafo = odl.tomo.RayTransform(space, geometry, impl='astra_cuda')

fbp_operator = odl.tomo.fbp_op(ray_trafo,
                               filter_type='Hann', frequency_scaling=0.7)

fbp_reconstruction = fbp_operator(data[0])
fbp_reconstruction.show('fbp_reconstruction 0')
fbp_reconstruction = fbp_operator(data[1])
fbp_reconstruction.show('fbp_reconstruction 1')
