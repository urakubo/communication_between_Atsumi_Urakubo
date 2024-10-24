import os, sys, copy, pprint
import numpy as np

from multiprocessing import Process, Pool, cpu_count, Queue, freeze_support
import queue

import configuration as c
import src.utils as u
import src.utils_graph as u_graph
import src.model_simulation as m

'''
def worker_q(input_q, output_q):
	for arg in iter(input_q.get, 'STOP'):
		result = m.create_simulation(arg)
		output_q.put(result)
	print('Get STOP singal.')
'''

if __name__ == "__main__":
	
	
	mode    = 'sic' # 'sic', 'bac', 'ttx'
	dist_id = 1     # 0, ..., 11
	num_cpu = 32
	p  = c.set_params(mode, dist_id)
	filename_data = p['dir_data'] + os.sep + 'distid_{}_mode_{}'.format(dist_id, mode)
	input_amp, v_apic_max, input_amp_th = u.load(filename_data) 
	u_graph.plot_i_v(input_amp, v_apic_max, p)
        
	'''
	# Set params
	p            = c.set_params(mode, dist_id)
	wrapped_args = c.set_args_for_each_run(p)
	
	print('Example parameters for a run')
	pprint.pprint(wrapped_args[0])

	os.makedirs(p['dir_data'], exist_ok=True)
	os.makedirs(p['dir_imgs'], exist_ok=True)

	# Single process
	for arg in wrapped_args:
		m.create_simulation(arg)
	
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
	u_graph.plot_i_v(input_amp, v_apic_max, p)
	u_graph.plot_i_v2(input_amp, v_apic_max, p)
	u_graph.plot_Ith_for_V_timing_dependence(input_amp_th, p)
	'''

	'''
	# Simulation under multiple distances (dist_ids)
	for dist_id in range(6,12):
		p            = c.set_params(mode, dist_id)
		wrapped_args = c.set_args_for_each_run(p)
		with Pool(num_cpu) as pool:
			output = pool.map(m.create_simulation, wrapped_args)

		g1 = u_graph.PlotProfiles( p )
		g1.run()

		filename_data = p['dir_data'] + os.sep + 'distid_{}_mode_{}'.format(dist_id, mode)
		g2 = u.I_V( p )
		g2.run()
		data  = (g2.input_amp, g2.v_apic_max, g2.input_amp_th)
		u.save(filename_data, data)
	
	for dist_id in range(12):
		p = c.set_params(mode, dist_id)
		filename_data = p['dir_data'] + os.sep + 'distid_{}_mode_{}'.format(dist_id, mode )
		input_amp, v_apic_max, input_amp_th = u.load(filename_data) 
		#u_graph.plot_i_v(input_amp, v_apic_max, p)
		u_graph.plot_i_v2(input_amp, v_apic_max, p)
		#u_graph.plot_Ith_for_V_timing_dependence(input_amp_th, p)
	'''
	
        
	'''
	freeze_support()
	input_q   = Queue()
	output_q  = Queue()
	for arg in wrapped_args:
		input_q.put( arg )
	num_cpu = 30
	for i in range(num_cpu):
		p = Process( target=worker_q, args=(input_q, output_q)).start()
		p.start()
	print('Results:')
	for i in range(len(wrapped_args)):
		print( '\t', output_q.get() )
	for i in range(num_cpu):
		input_q.put('STOP')

	p.join()
	'''
