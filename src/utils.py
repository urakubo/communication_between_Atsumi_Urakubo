import os, sys, pickle, copy
import numpy as np

def save(filename, data):
	with open(filename+'.pickle', mode='wb') as f:
		pickle.dump(data, f)
	return


def load(filename):
	with open(filename+'.pickle', mode='rb') as f:
		data = pickle.load(f)
	return data


class RepeatHandler():
	def __init__(self, p):
		self.p = p
	def run(self):
		self.dist_id  = self.p['dist_id']
		self.dir_data = self.p['dir_data']
		self.dir_imgs = self.p['dir_imgs']
		self.Vth      = self.p['Vth']
		self.preprocessing()
		for self.stim_type, self.i_soma_amp in self.p['i_soma_amps'].items():
			for self.i_dend_delay in self.p['i_dend_delays'][self.stim_type]:
				self.preprocessing_dend_amp()
				for self.i_dend_amp in self.p['i_dend_amps'][self.stim_type]:
					self.function()
				self.postprocessing_dend_amp()
	def preprocessing(self):
		pass
	def preprocessing_dend_amp(self):
		pass
	def function(self):
		pass
	def postprocessing_dend_amp(self):
		pass
	def get_filename_simdata(self):
		return self.dir_data + os.sep + \
				'distid{}_stimtype_{}_dend_Idelay{}_dend_Iamp{:.2f}'.\
				format( self.dist_id, self.stim_type, str(self.i_dend_delay).replace('-','m'), self.i_dend_amp )
	def get_filename_fig(self):
		return self.dir_imgs + os.sep + \
				'distid{}_stimtype_{}_dend_Idelay{}'.\
				format( self.dist_id, self.stim_type, str(self.i_dend_delay).replace('-','m') )


class WrappedAs(RepeatHandler):
	def __init__(self, p, a):
		RepeatHandler.__init__(self, p)
		self.a = a
	def preprocessing(self):
		self.wrapped_as = []
		
	def function(self):
		self.a['i_soma_amp']   = self.i_soma_amp
		self.a['i_dend_delay'] = self.i_dend_delay
		self.a['i_dend_amp']   = self.i_dend_amp
		self.a['filename']     = self.get_filename_simdata()
		self.wrapped_as.append( copy.deepcopy(self.a) )


class I_V(RepeatHandler):
	def __init__(self, p):
		RepeatHandler.__init__(self, p)
		
	def preprocessing(self):
		tmp_stims   = {s: {d: [] for d in self.p['i_dend_delays'][s] } for s in self.p['stim_types']}
		self.v_apic_max = copy.deepcopy(tmp_stims)
		self.input_amp  = copy.deepcopy(tmp_stims)
		tmp_stims   = {s: {d: 0 for d in self.p['i_dend_delays'][s] } for s in self.p['stim_types']}
		self.input_amp_th  = copy.deepcopy(tmp_stims)
		
	def function(self):
		filename  = self.get_filename_simdata()
		loaded = load(filename)
		self.v_apic_max[self.stim_type][self.i_dend_delay].append(loaded['v_apic_max'])
		self.input_amp[self.stim_type][self.i_dend_delay].append(loaded['input_amp'])

	def postprocessing_dend_amp(self):
		I_dend = np.array( self.input_amp[self.stim_type][self.i_dend_delay] )
		V_dend = np.array( self.v_apic_max[self.stim_type][self.i_dend_delay] )
		Vth    = self.Vth
		#print("V_dend ", V_dend )
		#print("V_dend - Vth ", V_dend - Vth)
		if np.all(V_dend - Vth < 0) or np.all(V_dend - Vth >= 0):
			self.input_amp_th[self.stim_type][self.i_dend_delay] = np.nan
		else:
			id  = np.where((V_dend - Vth > 0))[0][0]
			I1  = I_dend[id]
			I0  = I_dend[id-1]
			V1  = V_dend[id]
			V0  = V_dend[id-1]
			self.input_amp_th[self.stim_type][self.i_dend_delay] = ( I1*(Vth-V0) + I0*(V1-Vth) ) / (V1 - V0)

