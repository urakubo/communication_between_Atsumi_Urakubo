import os, sys, copy, pprint
import numpy as np

from neuron import h, gui
from neuron import coreneuron
coreneuron.enable = True
h.load_file("import3d.hoc")
#h.load_file("printCell.hoc")


import bin.utils as u
import bin.utils_graph as u_graph


def apply_soma_ttx(cell):
	targ_cell_lists = (cell.somatic, cell.apical) # cell.basal
	for secs in targ_cell_lists:
		for sec in secs:
			for seg in sec:
				if h.distance(seg.x, sec=sec) < 50:
					sec(seg.x).gNaTs2_tbar_NaTs2_t = sec(seg.x).gNaTs2_tbar_NaTs2_t /20
	
	for sec in cell.axonal:
		for seg in sec:
			if h.distance(seg.x, sec=sec) < 50:
				sec(seg.x).gNaTa_tbar_NaTa_t = sec(seg.x).gNaTa_tbar_NaTa_t /20
				sec(seg.x).gNap_Et2bar_Nap_Et2 = sec(seg.x).gNap_Et2bar_Nap_Et2 /20


def distance_gIh(dist):
	return 0.25 * 0.01*(1+np.cos(dist/1000*2*np.pi*2))
	
def create_cell():
	
	# Shape
	
	biophysicalModelFilename = "./model/Leleo_Segev/L5PCbiophys5b.hoc"
	biophysicalModelTemplateFilename = "./model/Leleo_Segev/L5PCtemplate_2.hoc"
	morphologyFilename = "./model/Leleo_Segev/morphologies/cell1.asc"
	
	
	h.load_file(biophysicalModelFilename)
	h.load_file(biophysicalModelTemplateFilename)
	L5PC = h.L5PCtemplate(morphologyFilename)
	
	h.distance(0, sec=L5PC.soma[0])
	
	
	'''
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
	
	# Create section lists "apical tufts" and "apical trunk"
	list_tuft = h.SectionList()
	list_tuft.subtree(sec=L5PC.apic[36])
	list_tuft.remove(sec=L5PC.apic[36])

	list_trunk = h.SectionList()
	for id_sec in [0,1,2,3,4,14,20,26,34,36]:
		list_trunk.append(L5PC.apic[id_sec])
		# print('L5PC.apic[{}], distance: {}'.format( id_sec, h.distance(0.5, sec=L5PC.apic[id_sec]) ) )

	list_soma  = h.SectionList()
	for sec in h.allsec():
		if h.distance(0.5, sec=sec) < 50:
			# print('distance: ', h.distance(0.5, sec=sec) )
			list_soma.append(sec)
	
	print('L5PC created!')
	
	return L5PC, list_tuft, list_trunk, list_soma


def run_simulation():
	h.cvode.active(0)
	print("tstop : ", h.tstop)
	h.dt = 0.05
	h.finitialize(-80)
	h.run()


class Recording():
	def __init__(self, cell, current_soma, current_dend, arg):
		
		i_sec_id  = arg['i_dend_sec_id']
		i_seg     = arg['i_dend_seg']
		targ_v_recording_dend = cell.apic[i_sec_id]( i_seg ) #  cell.apic[36](0.5)
		self.recs = {
			't':{'target': h._ref_t},
			'v_soma':{'target': cell.soma[0](0.5)._ref_v },
			'v_apic':{'target': targ_v_recording_dend._ref_v},
			'i_soma':{'target': current_soma._ref_i},
			'i_dend':{'target': current_dend._ref_i}}
		for rec in self.recs.values():
			rec['data'] = h.Vector().record(rec['target'])
		
		self.all = {}
		self.i_all = []
		self.time_prerun = arg['time_prerun']
		self.onset_for_peak_detecion = arg['time_onset_for_v_peak_detection_after_prerun']

	def clear_all(self):
		self.all = {}
		self.i_all = []

	def postprocessing(self, input_amp):
		self.data = { k: np.array(v['data']) for k, v in self.recs.items() }
		self.data['input_amp'] = input_amp
		flag = (np.array(self.recs['t']['data']) >= self.time_prerun + self.onset_for_peak_detecion)
		tmp = np.array(self.recs['v_apic']['data'])
		self.data['v_apic_max'] = np.max( tmp[flag] )


def create_simulation(arg):
	
	print('Somatic current: {}, Dendritic loc: {}, i_dend_delay: {}'.format( \
		arg['i_soma_amp'], arg['dist'], arg['i_dend_delay'] ) )
	
	h.tstop = arg['time_prerun'] + arg['time_run_after_prerun']
	
	# Initialization
	L5PC, list_tuft, list_trunk, list_soma = create_cell()
	h.distance(0, sec=L5PC.soma[0])
	
	#
	if 'apply_soma_ttx' in arg.keys() and arg['apply_soma_ttx'] == True:
		apply_soma_ttx(L5PC)
	
	# Somatic current
	current_soma = h.IClamp(0.5, sec=L5PC.soma[0] )
	current_soma.delay = arg['time_prerun']
	current_soma.dur   = arg['i_soma_duration']
	current_soma.amp   = arg['i_soma_amp'] 
	
	# Dendritic current
	sec_id = arg['i_dend_sec_id']
	seg    = arg['i_dend_seg']
	current_dend       = h.IClamp(seg, sec=L5PC.apic[sec_id] )
	current_dend.delay = arg['time_prerun'] + arg['i_soma_duration'] + arg['i_dend_delay']
	current_dend.dur   = 50
	current_dend.amp   = arg['i_dend_amp']
	
	# Set recording
	rec = Recording(L5PC, current_soma, current_dend, arg)
	
	run_simulation()
	
	# Save data
	rec.postprocessing(arg['i_dend_amp'] )
	u.save(arg['filename'], rec.data)
	
	
