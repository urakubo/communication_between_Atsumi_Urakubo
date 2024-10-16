import os, sys, copy, pprint
import numpy as np

from multiprocessing import Pool, cpu_count

import configuration as c
import bin.utils as u
import bin.utils_graph as u_graph
import bin.model_simulation as m


if __name__ == "__main__":
	
	
	sim_type = 'sic' # 'sic', 'bac', 'ttx'
	dist_id = 4     # 0, ..., 11
	
	p            = c.set_params(sim_type, dist_id)
	wrapped_args = c.set_args_for_each_run(p)
	
	'''
	print('All parameters for the simulation')
	pprint.pprint(p)
	'''
	
	print('Example parameters for a run')
	pprint.pprint(wrapped_args[0])
	
	os.makedirs(p['dir_data'], exist_ok=True)
	os.makedirs(p['dir_imgs'], exist_ok=True)
	
	#m.create_simulation(wrapped_args[0]) # Single process
	
	'''
	with Pool(4) as pool: # Multiple process
		output = pool.map(m.create_simulation, wrapped_args)
	'''
	
	
	# Graph plot
	#'''
	g1 = u_graph.PlotProfiles( p )
	g1.run()
	#'''
	
	g2 = u.I_V( p )
	g2.run()
	u_graph.plot_i_v(g2.input_amp, g2.v_apic_max, p)
	
	
	
