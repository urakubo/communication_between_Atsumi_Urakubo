import os, sys
import src.utils as u


def set_params(mode, dist_id, distrib_h = ''):
	
	# Shared model parameters 
	p = {}
	
	# Location for dendritic stimulation
	p['dists']          = [100.385, 199.595, 306.988, 390.955, 504.155, 598.4877,699.3115,805.2813,890.0572,1008.6173,1085.7455,1199.4136 ]
	p['i_dend_sec_ids'] = [1, 14, 26, 36, 36,   36, 60, 60, 60, 61, 61, 63]
	p['i_dend_segs']    = [0.833,0.166,0.5,0.03846,0.5, 0.8846, 0.0455, 0.5000, 0.8636, 0.5000, 0.9444, 0.3889 ]
	
	if dist_id not in range(12):
		print('Invalid dist_id: ', dist_id)
		sys.exit(1)
	p['dist_id']       = dist_id
	p['dist']          = p['dists'][ dist_id ]
	p['i_dend_sec_id'] = p['i_dend_sec_ids'][ dist_id ]
	p['i_dend_seg']    = p['i_dend_segs'][ dist_id ]
	
	
	if dist_id in [10, 11]:
		p['amps'] = [0.01 * i for i in range(0,30)] # dist_id = 10 (1100 um)
		p['Vth']  = -20		
	elif dist_id in [7, 8, 9]:
		p['amps'] = [0.01 * i for i in range(0,40)] # dist_id = 7 (800 um), 8 (900 um), 9 (1000 um) 
		p['Vth']  = -20		
	elif dist_id in [6]:
		p['amps'] = [0.02 * i for i in range(0,30)] # dist_id = 6 (700 um),
		p['Vth']  = -20		
	elif dist_id in [4, 5]:
		id_amp_start = 0 if mode == 'bac' else 10
		p['amps'] = [0.02 * i for i in range(id_amp_start, 40)] # dist_id = 4 (500 um), 5 (600 um)
		p['Vth']  = -20		
	elif dist_id in [2,3]:
		id_amp_start = 0 if mode == 'bac' else 20
		p['amps'] = [0.02 * i for i in range(id_amp_start, 50)] # dist_id = 3 (400 um),  2 (300 um),
		p['Vth']  = -20
	elif dist_id in [0,1]:
		id_amp_start = 0 if mode == 'bac' else 20
		p['amps'] = [0.02 * i for i in range(id_amp_start, 50)] # dist_id = 1 (200 um),  0 (100 um),
		p['Vth']  = -40
	
	
	p['mode'] = mode
	if  mode == 'sic':
		p['dir_data']        = 'data_I'
		p['dir_imgs']        = 'imgs_I'
		p['dir_imgs_summary']= 'imgs_I_summary'
		p['stim_types']      = ['soma_only', 'dend_only', 'soma_and_dend']
		p['i_dend_delays']   = {'soma_only': [0],  'dend_only': [0]      , 'soma_and_dend':list(range(-80, 90, 10)) }
		p['i_dend_amps']     = {'soma_only': [0],  'dend_only': p['amps'], 'soma_and_dend':p['amps'] }
		p['i_soma_amps']     = {'soma_only': -0.5, 'dend_only': 0        , 'soma_and_dend': -0.5 }
		p['i_soma_duration'] = 150
		p['apply_soma_ttx']  = False
		
	elif mode == 'ttx':
		p['dir_data']        = 'data_I_ttx'
		p['dir_imgs']        = 'imgs_I_ttx'
		p['dir_imgs_summary']= 'imgs_I_ttx_summary'
		p['stim_types']      = ['soma_only', 'dend_only', 'soma_and_dend']
		p['i_dend_delays']   = {'soma_only': [0],  'dend_only': [0]      , 'soma_and_dend':list(range(-80, 90, 10)) }
		p['i_dend_amps']     = {'soma_only': [0],  'dend_only': p['amps'], 'soma_and_dend':p['amps'] }
		p['i_soma_amps']     = {'soma_only': -0.5, 'dend_only': 0        , 'soma_and_dend': -0.5 }
		p['i_soma_duration'] = 150
		p['apply_soma_ttx']  = True
		
	elif mode == 'bac':
		p['dir_data']        = 'data_I_bac'
		p['dir_imgs']        = 'imgs_I_bac'
		p['dir_imgs_summary']= 'imgs_I_bac_summary'
		p['stim_types']      = ['soma_only', 'dend_only', 'soma_and_dend']
		p['i_dend_delays']   = {'soma_only': [0], 'dend_only': [0]      , 'soma_and_dend':list(range(-80, 90, 10)) }
		p['i_dend_amps']     = {'soma_only': [0], 'dend_only': p['amps'], 'soma_and_dend':p['amps'] }
		p['i_soma_amps']     = {'soma_only': 1.5, 'dend_only': 0        , 'soma_and_dend': 1.5 }
		p['i_soma_duration'] = 5
		p['apply_soma_ttx']  = False
		# Shai2015 1.4 somatic spiking, 1.3 nA ... non somatic spiking.
	else :
		print('Invalid mode: ', mode)
		sys.exit(1)
	
	
	# Variation of h channel distribution
	if distrib_h in ['reverse','uniform','none']:
		p['dir_data']        += '_Ih_'+distrib_h
		p['dir_imgs']        += '_Ih_'+distrib_h
		p['dir_imgs_summary']+= '_Ih_'+distrib_h
		p['distrib_h'] = distrib_h
	elif distrib_h != '':
		print('Invalid distrib_h: ', distrib_h)
		sys.exit(1)
	
	
	# Simulation time
	p['time_prerun']                     = 550
	p['time_run_after_prerun']           = 400
	p['time_onset_for_v_peak_detection'] = 450
	p['time_set_zero'] = p['time_prerun'] + p['i_soma_duration']
	return p


def set_args_for_each_run(p):
	# a: Parameters used for each run of simulation ( used in create_simulation )
	a = {}
	
	a['i_soma_duration'] = p['i_soma_duration']
	a['apply_soma_ttx']  = p['apply_soma_ttx']
	
	a['i_dend_sec_id']   = p['i_dend_sec_id']
	a['i_dend_seg']      = p['i_dend_seg']
	
	a['time_prerun']     = p['time_prerun']
	a['time_run_after_prerun'] = p['time_run_after_prerun']
	a['time_onset_for_v_peak_detection'] = p['time_onset_for_v_peak_detection']
	
	a['Vth']  = p['Vth']
	
	# Deferent values for each run
	a['i_soma_amp']   = 0
	a['i_dend_delay'] = 0
	a['i_dend_amp']   = 0
	a['filename']     = ''
	
	if 'distrib_h' in p.keys():
		a['distrib_h']     = p['distrib_h']
	
	w = u.WrappedAs(p, a)
	w.run()
	wrapped_as = w.wrapped_as
	
	return wrapped_as


rc_param = {'pdf.fonttype' : 'truetype',
	'svg.fonttype' : 'none',
	'font.family' : 'sans-serif',
	'font.sans-serif' : 'Arial',
	'font.style' : 'normal',
	'axes.spines.right' : False,
	'axes.spines.top' : False,
	'legend.frameon': False}

