
# python -i main_check_loc_distance.py

# Line 2 was used to exmaine distance dependence (see configuration.py).

import os, sys, copy
import numpy as np

from neuron import h, gui
from neuron import coreneuron
coreneuron.enable = True
h.load_file("import3d.hoc")
#h.load_file("printCell.hoc")

import src.model_simulation as m

if __name__ == "__main__":
	
	
	L5PC, list_tuft, list_trunk, list_soma = m.create_cell()
	h.distance(0, sec=L5PC.soma[0])
	
	h.topology()
	
	Line1 = [0,1,2,3,4,14,20,26,34,36,37,38,40,44]
	Line2 = [0,1,2,3,4,14,20,26,34,36,50,60,61,62,63]
	
	for id_sec in Line2:
		for seg in L5PC.apic[id_sec]:
			dist = h.distance(1, L5PC.apic[id_sec](seg.x))
			print('{:.0f} L5PC.apic[{}], {:.4f}, {:.4f} um (dist from soma)'.format(round(dist, -2), id_sec, seg.x, dist))
	
	
	# Line1
	# Close to 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200 um
	# 100 L5PC.apic[1], 0.8333, 100.3854 um
	# 200 L5PC.apic[14], 0.1667, 199.5957 um
	# 300 L5PC.apic[26], 0.5000, 306.9882 um
	# 400 L5PC.apic[36], 0.0385, 390.9557 um
	# 500 L5PC.apic[36], 0.5000, 504.1550 um
	# 600 L5PC.apic[36], 0.8846, 598.4877 um
	
	# 700 L5PC.apic[37], 0.2692, 701.1962 um
	# 800 L5PC.apic[37], 0.6538, 807.4942 um
	# 900 L5PC.apic[37], 0.9615, 892.5326 um
	# 1000 L5PC.apic[40], 0.0455, 999.4725 um
	# 1100 L5PC.apic[40], 0.5000, 1092.8462 um
	# 1200 L5PC.apic[44], 0.1000, 1203.9748 um
	
	#dists = [100.385, 199.595, 306.988, 390.955, 504.155, 598.488, \
	#		701.196, 807.494, 892.533, 999.473, 1092.846, 1203.975]
	#ids_sec = [1, 14, 26, 36, 36, 36,    37, 37, 37, 40, 40, 44]
	#segs  = [0.833,0.166,0.5,0.03846,0.5,0.885,   0.269,0.654,0.962,0.04545,0.5,0.1]
	
	
	
	# Line2
	# Close to 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200 um
	# 100 L5PC.apic[1], 0.8333, 100.3854 um
	# 200 L5PC.apic[14], 0.1667, 199.5957 um
	# 300 L5PC.apic[26], 0.5000, 306.9882 um
	# 400 L5PC.apic[36], 0.0385, 390.9557 um
	# 500 L5PC.apic[36], 0.5000, 504.1550 um
	# 600 L5PC.apic[36], 0.8846, 598.4877 um
	
	# 700 L5PC.apic[60], 0.0455, 699.3115 um
	# 800 L5PC.apic[60], 0.5000, 805.2813 um
	# 900 L5PC.apic[60], 0.8636, 890.0572 um
	# 1000 L5PC.apic[61], 0.5000, 1008.6173 um
	# 1100 L5PC.apic[61], 0.9444, 1085.7455 um
	# 1200 L5PC.apic[63], 0.3889, 1199.4136 um
	
	dists = [100.385, 199.595, 306.988, 390.955, 504.155, 598.4877,\
		699.3115,805.2813,890.0572,1008.6173,1085.7455,1199.4136 ]
	ids_sec = [1, 14, 26, 36, 36, 36,   60, 60, 60, 61, 61, 63]
	segs  = [0.833,0.166,0.5,0.03846,0.5, 0.8846,   0.0455, 0.5000, 0.8636, 0.5000, 0.9444, 0.3889 ]
	
	
	
	# Visualization
	list_sites_synaptic_input = []
	for id_sec, seg in zip(ids_sec, segs):
		list_sites_synaptic_input.append(h.AlphaSynapse(L5PC.apic[id_sec](seg)))
	
	shape_dend = h.Shape()
	marker_size = 10
	for syn in list_sites_synaptic_input:
		shape_dend.point_mark(syn,2,"O",marker_size)
	# 0 white, 1 black, 2 red, 3 blue, 4 green, 5 orange, 6 brown, 7 violet, 8 yellow, 9 gray
	
	mleft, mbottom = -541.0, -226.554
	mwidth, mheight = 611.846-mleft, 1218.9-mbottom
	sleft, sbottom, swidth, sheight = 200, 900, 800, 1000
	shape_dend.view(mleft, mbottom, mwidth, mheight, sleft, sbottom, swidth, sheight)
	shape_dend.show( 0 )
	# 0: displays diameters
	# 1: line through all the 3d points
	# 2: line through 1st and last 2d points of
	
	
	