
# python -i main_check_channel_distribution.py
import os, sys, copy, pickle
import numpy as np
import matplotlib.pyplot as plt

from neuron import h
from neuron import coreneuron
coreneuron.enable = True
h.load_file("import3d.hoc")


import src.utils as u
import src.utils_graph as u_graph
import src.model_simulation as m


def calc_distance_gIhbar(distance, maxLength):
	
	x1 = 4
	x3 = -0.8696
	x4 = 3.6161
	x5 = 0.0
	x6 = 2.0870
	x7 = 0.00010000000
	
	th = 0.65
	x2 = distance / maxLength
	x2 = (x2 > th) * th + (x2 <= th) * x2
	
	value = x7 * ( x3 + x6*np.exp(x4*(x2-x5)) )
	return value
	
	
	
def get_distance_gIhbar(targ_cell_lists, dist_scale = 1):
	distance = []
	density  = []
	for secs in targ_cell_lists:
		for sec in secs:
			for seg in sec:
				distance.append( h.distance(seg.x, sec=sec) * dist_scale )
				density.append(  sec(seg.x).gIhbar_Ih  )
	return distance, density
	
	
def plot_a_dist_density(ax, distance, density, col, label):
	markersize = 2
	ax.plot(distance, density, 'o',
				markersize=markersize, 
				markerfacecolor=col, 
				markeredgecolor=col,
				markeredgewidth=1,
				label = label)
	
	
def plot_distance_gIhbar(L5PC):
	
	# Get modeled density for each compartment.
	targ_cell_lists = (L5PC.somatic, L5PC.apical)
	apical_distance, apical_density = get_distance_gIhbar(targ_cell_lists)
	targ_cell_lists = (L5PC.basal,)
	basal_distance, basal_density = get_distance_gIhbar(targ_cell_lists, dist_scale = -1) # 0.0001/2
	targ_cell_lists = (L5PC.axonal,)
	axonal_distance, axonal_density = get_distance_gIhbar(targ_cell_lists) # 0.0001/2
	
	# Calc theoretial densities.
	max_apical_length = L5PC.getLongestBranch("apic")
	distance = np.linspace(0, max_apical_length, 50)
	density  = calc_distance_gIhbar(distance, max_apical_length)
	
	print('distance ', distance)
	print('density  ', density)
	
	
	fig = plt.figure(constrained_layout=True, figsize=(4.0, 3.0))
	ax  = fig.add_subplot()
	ax.set_xlabel('Distance from soma (um)')
	ax.set_ylabel('gIhbar_Ih (mA/cm2)')
	
	ax.plot(distance, density, ':', linewidth = 5,color = '#f781bf')
	
	plot_a_dist_density(ax, apical_distance, apical_density, 'r', 'Apical')
	plot_a_dist_density(ax, basal_distance , basal_density , 'b', 'Basal' )
	plot_a_dist_density(ax, axonal_distance, axonal_density, 'k', 'Axonal')
	
	
	ax.legend()
	dir_imgs = 'imgs_setup'
	filename = 'distrib_Ih'
	os.makedirs(dir_imgs, exist_ok=True)
	u_graph.savefig_showfig(filename, dir_imgs)
	
	
	
	
if __name__ == "__main__":
	
	L5PC, list_tuft, list_trunk, list_soma = m.create_cell()
	h.distance(0, sec=L5PC.soma[0])
	
	
	plot_distance_gIhbar(L5PC)
	
	
	'''
	
	ps = h.PlotShape(True)	
	# Ih current
	# gIhbar_Ih = 0.001
	
	ps.variable('gIhbar_Ih')
	ps.scale(0, 0.005)
	
	
	mleft, mbottom = -541.0, -226.554
	mwidth, mheight = 611.846-mleft, 1218.9-mbottom
	sleft, sbottom, swidth, sheight = 200, 900, 800, 1000
	ps.view(mleft, mbottom, mwidth, mheight, sleft, sbottom, swidth, sheight)
	ps.show(0)
	ps.exec_menu('Shape Plot')
	
	# Ih distribution
	max_apical_length = L5PC.getLongestBranch("apic")
	print('max_apical_length ', max_apical_length)
	
	
	for sec in L5PC.somatic:
		sec.gIhbar_Ih = 0.01
	for sec in L5PC.apical:
		for seg in sec:
			dist = h.distance(1, sec(seg.x))
			sec(seg.x).gIhbar_Ih = distance_gIh(dist)
	'''
	
	
	
	
	