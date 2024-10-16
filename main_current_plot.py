import os, sys
import numpy as np

import argparse
import code
import pprint

import configuration as c
import bin.utils as u
import bin.utils_graph as u_graph
import bin.model_simulation as m

import matplotlib.pyplot as plt
plt.rcParams.update( c.rc_param )
	
	
	
	
if __name__ == "__main__":
	
	
	sim_type = 'sic' # 'sic', 'bac', 'ttx'
	dist_id  = 4     # 0, ..., 11
	p        = c.set_params(sim_type, dist_id)
	filename_data = p['dir_data'] + os.sep + 'distid_{}_simtype_{}'.format(dist_id, sim_type )
	
	# Get peak amplitudes of membrane potentials
	'''
	g2 = u.I_V( p )
	g2.run()
	data  = (g2.input_amp, g2.v_apic_max, g2.input_amp_th)
	u.save(filename_data, data)
	'''
	input_amp, v_apic_max, input_amp_th = u.load(filename_data) 
	
	
	#
	# Plot timing dependence
	#
	u_graph.plot_i_v2(input_amp, v_apic_max, p)
	u_graph.plot_Ith_for_V_timing_dependence(input_amp_th, p)
	
	