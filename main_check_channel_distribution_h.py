
# python -i main_check_channel_distribution.py
import os, sys, copy, time
import numpy as np
import matplotlib.pyplot as plt

from neuron import h
from neuron import coreneuron
coreneuron.enable = True
h.load_file("import3d.hoc")


import src.utils as u
import src.utils_graph as u_graph
import src.model_simulation as m


# axonal  0.0001/2
# somatic 0.0001*0.75
# basal   0.0001/2 

def calc_gIhbar_org(distance, maxLength):
	x1 = 4
	x3 = -0.8696
	x4 = 3.6161
	x5 = 0.0
	x6 = 2.0870
	x7 = 0.00010000000
	
	th = 0.65
	x2 = distance / maxLength
	x2 = (x2 > th) * th + (x2 >= 0) * (x2 <= th) * x2 + (x2 < 0) * 0.0001/2
	
	value = x7 * ( x3 + x6*np.exp(x4*(x2-x5)) )
	return value

def calc_gIhbar_rev(distance, maxLength):
	x1 = 4
	x3 = -0.8696
	x4 = 3.6161
	x5 = 0.0
	x6 = 2.0870
	x7 = 0.00010000000
	
	th = 0.65
	x2 = distance / maxLength
	x2 = (x2 > th) * th + (x2 >= 0) * (x2 <= th) * x2 + (x2 < 0) * 0
	
	value = x7 * ( x3 + x6*np.exp(x4*(th-(x2-x5))) )
	return value
	
def calc_gIhbar_none(distance, maxLength):
	return 0.0*distance
	
	
def calc_gIhbar_uniform(distance, maxLength, gIhbar = 0.001):
	return 0.0*distance + gIhbar
	
	
def set_gIhbar(L5PC, calc_gIhbar):
	maxLength = L5PC.getLongestBranch("apic")
	for secs in (L5PC.somatic, L5PC.apical):
		for sec in secs:
			for seg in sec:
				distance = h.distance(seg.x, sec=sec)
				sec(seg.x).gIhbar_Ih = calc_gIhbar(distance, maxLength)

	for secs in (L5PC.basal, L5PC.axonal):
		for sec in secs:
			for seg in sec:
				distance = h.distance(seg.x, sec=sec) * (-1)
				sec(seg.x).gIhbar_Ih = calc_gIhbar(distance, maxLength)
	return True
	
	
	
def plot_model_gIhbar(L5PC, dir_imgs):
	# Calc modeled densities.
	max_apical_length = L5PC.getLongestBranch("apic")
	distance      = np.linspace(-max_apical_length/2, max_apical_length, 50)
	density_org   = calc_gIhbar_org(distance, max_apical_length)
	density_rev   = calc_gIhbar_rev(distance, max_apical_length)
	density_none  = calc_gIhbar_none(distance, max_apical_length)
	density_const = calc_gIhbar_uniform(distance, max_apical_length)

	# Plot.
	fig = plt.figure(constrained_layout=True, figsize=(4.0, 3.0))
	ax  = fig.add_subplot()
	ax.set_xlabel('Distance from soma (um)')
	ax.set_ylabel('gIhbar_Ih (mA/cm2)')
	
	lw = 2
	alpha = 0.3
	ax.plot(distance, density_org  , '-', linewidth = lw,color = (alpha,alpha,alpha), label = 'control')
	ax.plot(distance, density_none , '-', linewidth = lw,color = (alpha,alpha,1), label = 'none')
	ax.plot(distance, density_rev  , '-', linewidth = lw,color = (alpha,1,alpha), label = 'reverse')
	ax.plot(distance, density_const, '-', linewidth = lw,color = (1,alpha,alpha), label = 'uniform')
	
	ax.legend()
	dir_imgs = 'imgs_setup'
	filename = 'distrib_Ih_model'
	os.makedirs(dir_imgs, exist_ok=True)
	u_graph.savefig_showfig(filename, dir_imgs)
	
	
def get_gIhbar_org(targ_cell_lists, dist_scale = 1):
	distance = []
	density  = []
	for secs in targ_cell_lists:
		for sec in secs:
			for seg in sec:
				distance.append( h.distance(seg.x, sec=sec) * dist_scale )
				density.append(  sec(seg.x).gIhbar_Ih  )
	return distance, density
	
	
	
def plot_measured_gIhbar(L5PC, dir_imgs):
	
	# Get gIhbar densities from the compartments.
	targ_cell_lists = (L5PC.somatic, L5PC.apical)
	apical_distance, apical_density = get_gIhbar_org(targ_cell_lists)
	targ_cell_lists = (L5PC.basal,)
	basal_distance, basal_density   = get_gIhbar_org(targ_cell_lists, dist_scale = -1) # 0.0001/2
	targ_cell_lists = (L5PC.axonal,)
	axonal_distance, axonal_density = get_gIhbar_org(targ_cell_lists) # 0.0001/2
	
	# Plot.
	fig = plt.figure(constrained_layout=True, figsize=(4.0, 3.0))
	ax  = fig.add_subplot()
	ax.set_xlabel('Distance from soma (um)')
	ax.set_ylabel('gIhbar_Ih (mA/cm2)')
	
	
	data_points = [\
		(apical_distance, apical_density, 'r', 'Apical'),\
		(basal_distance , basal_density , 'b', 'Basal'),\
		(axonal_distance, axonal_density, 'k', 'Axonal')\
		]
	for distance, density, col, label in data_points:
		markersize = 2
		ax.plot(distance, density, 'o',
				markersize=markersize, 
				markerfacecolor=col, 
				markeredgecolor=col,
				markeredgewidth=1,
				label = label)
	
	ax.legend()

	filename = 'distrib_Ih_measured'
	u_graph.savefig_showfig(filename, dir_imgs)
	
	
def plot_shape_h():
	
	from neuron import gui
	ps = h.PlotShape(True)
	
	ps.variable('gIhbar_Ih')
	ps.scale(0, 0.005)
	
	mleft, mbottom = -541.0, -226.554
	mwidth, mheight = 611.846-mleft, 1218.9-mbottom
	sleft, sbottom, swidth, sheight = 200, 900, 800, 1000
	ps.view(mleft, mbottom, mwidth, mheight, sleft, sbottom, swidth, sheight)
	ps.show(0)
	ps.exec_menu('Shape Plot')
	time.sleep(10)
	
	
if __name__ == "__main__":

	dir_imgs = 'imgs_preparation'
	os.makedirs(dir_imgs, exist_ok=True)
	
	L5PC, list_tuft, list_trunk, list_soma = m.create_cell()
	h.distance(0, sec=L5PC.soma[0])
	# plot_model_gIhbar(L5PC, dir_imgs)
	
	#set_gIhbar(L5PC, calc_gIhbar=calc_gIhbar_rev)
	set_gIhbar(L5PC, calc_gIhbar=calc_gIhbar_uniform)
	plot_measured_gIhbar(L5PC, dir_imgs)
	
	# plot_shape_h()
	
	
	
