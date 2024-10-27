import os, sys, copy, pprint
import numpy as np

from multiprocessing import Process, Pool, cpu_count, Queue, freeze_support
import queue

import configuration as c
import src.utils as u
import src.utils_graph as u_graph
import src.model_simulation as m


if __name__ == "__main__":
	
	
	mode    = 'bac' # 'sic', 'bac', 'ttx'
	dist_id = 4     # 0, ..., 11
	num_cpu = 32
	p  = c.set_params(mode, dist_id)
	os.makedirs(p['dir_data'], exist_ok=True)
	os.makedirs(p['dir_imgs'], exist_ok=True)
	os.makedirs(p['dir_imgs_summary'], exist_ok=True)
    
	
	# Set params
	p            = c.set_params(mode, dist_id)
	wrapped_args = c.set_args_for_each_run(p)
	
	print('Example parameters for a run')
	pprint.pprint(wrapped_args[0])

	'''
	# Single process
	#for arg in wrapped_args:
	#	m.create_simulation(arg)
	
	# Multiple processes
	with Pool(num_cpu) as pool:
		output = pool.map(m.create_simulation, wrapped_args)

	# Plot profiles
	g1 = u_graph.PlotProfiles( p )
	g1.run()
	
	# Get peak amplitudes of dendirtic membrane potentials
	filename_data = p['dir_data'] + os.sep + 'distid_{}_mode_{}'.format(dist_id, mode)
	g2 = u.I_V( p )
	g2.run()
	data  = (g2.input_amp, g2.v_apic_max, g2.input_amp_th)
	u.save(filename_data, data)


	# Plot Ca spike amplitudes and the timing dependence
	filename_data = p['dir_data'] + os.sep + 'distid_{}_mode_{}'.format(dist_id, mode)
	input_amp, v_apic_max, input_amp_th = u.load(filename_data) 


	pl = u_graph.PlotIforSpike(input_amp, v_apic_max, p)
	pl.repeat_plots()
	pl.plot_delays()
	
	#u_graph.plot_timing_dependent_i_for_spike(input_amp_xth, p)
	
	# Simulation with multiple distances (dist_ids)
	for dist_id in range(6):
		p            = c.set_params(mode, dist_id)
		wrapped_args = c.set_args_for_each_run(p)
		with Pool(num_cpu) as pool:
			output = pool.map(m.create_simulation, wrapped_args)
	'''

	for dist_id in range(12):
		p  = c.set_params(mode, dist_id)
		g1 = u_graph.PlotProfiles( p )
		g1.run()
	'''

	for dist_id in range(12):
		filename_data = p['dir_data'] + os.sep + 'distid_{}_mode_{}'.format(dist_id, mode)
		g2 = u.I_V( p )
		g2.run()
		data = (g2.input_amp, g2.v_apic_max, g2.input_amp_th)
		u.save(filename_data, data)
	for dist_id in range(12):
		p = c.set_params(mode, dist_id)
		filename_data = p['dir_data'] + os.sep + 'distid_{}_mode_{}'.format(dist_id, mode )
		input_amp, v_apic_max, input_amp_th = u.load(filename_data) 
		pl = u_graph.PlotIforSpike(input_amp, v_apic_max, p)
		#pl.plot_delays()
		pl.repeat_plots()
		#u_graph.plot_timing_dependent_i_for_spike(input_amp_th, p)

	'''
