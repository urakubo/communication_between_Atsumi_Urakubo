import os, sys, copy, pprint
import numpy as np

from multiprocessing import Pool, cpu_count

import configuration as c
import src.utils as u
import src.utils_graph as u_graph
import src.model_simulation as m


if __name__ == "__main__":
	
	
	sim_type = 'sic' # 'sic', 'bac', 'ttx'
	dist_id  = 7     # 0, ..., 11
	
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
	
	m.create_simulation(wrapped_args[0]) # Single process
	

	'''
	with Pool(30) as pool: # Multiple process
		output = pool.map(m.create_simulation, wrapped_args)
	'''
	
	
	# Plot profiles
	'''
	g1 = u_graph.PlotProfiles( p )
	g1.run()
	'''
	
	
	# Get peak amplitudes of dendirtic membrane potentials
	filename_data = p['dir_data'] + os.sep + 'distid_{}_simtype_{}'.format(dist_id, sim_type )
	'''
	g2 = u.I_V( p )
	g2.run()
	data  = (g2.input_amp, g2.v_apic_max, g2.input_amp_th)
	u.save(filename_data, data)
	'''
	input_amp, v_apic_max, input_amp_th = u.load(filename_data) 
	
	
	
	# Plot Ca spike amplitudes and the timing dependence
	'''
	u_graph.plot_i_v(g2.input_amp, g2.v_apic_max, p)
	u_graph.plot_i_v2(input_amp, v_apic_max, p)
	u_graph.plot_Ith_for_V_timing_dependence(input_amp_th, p)
	'''
	
