
# python -i main_check_channel_distribution.py

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
	ps = h.PlotShape(True)	
	
	# Na currents
  	# gNap_Et2bar_Nap_Et2 = 0.005834 
  	# gNaTa_tbar_NaTa_t = 3.89618 
	# gNaTs2_tbar_NaTs2_t = 0.998912 
	# gNaTs2_tbar_NaTs2_t = 0.998912 
	
	'''
	ps.variable('gNaTs2_tbar_NaTs2_t')
	ps.scale(0, 1.2)
	
	ps.variable('gNaTa_tbar_NaTa_t')
	ps.scale(0, 4.8)
	
	ps.variable('gNap_Et2bar_Nap_Et2')
	ps.scale(0, 0.012)
	'''

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
	
	
	
	'''
	# Workspace for the decrease of Na channels (ttx)
	targ_cell_lists = (L5PC.somatic, L5PC.apical) # cell.basal
	for secs in targ_cell_lists:
		for sec in secs:
			for seg in sec:
				if h.distance(seg.x, sec=sec) < 50:
					sec(seg.x).gNaTs2_tbar_NaTs2_t = sec(seg.x).gNaTs2_tbar_NaTs2_t /20
	
	for sec in L5PC.axonal:
		for seg in sec:
			if h.distance(seg.x, sec=sec) < 50:
				sec(seg.x).gNaTa_tbar_NaTa_t = sec(seg.x).gNaTa_tbar_NaTa_t /20
				sec(seg.x).gNap_Et2bar_Nap_Et2 = sec(seg.x).gNap_Et2bar_Nap_Et2 /20
	'''
	