import os, sys, glob, pickle
import numpy as np


import bin.utils as u
import configuration as c

import matplotlib.pyplot as plt

# Matplotlib
plt.rcParams.update( c.rc_param )


def initialize_fig_panel_profile(ax, ylabel='Membrane pot (mV)'):
	ax.spines['right'].set_visible(False)
	ax.spines['top'].set_visible(False)
	ax.set_xlabel('Time (ms)')
	ax.set_ylabel(ylabel)
	#ax.set_box_aspect(1)
	
	
def initialize_fig_panel_i_v(ax):
	ax.spines['right'].set_visible(False)
	ax.spines['top'].set_visible(False)
	ax.set_xlabel('Dendritic current injection (pA)')
	ax.set_ylabel('Peak amp of dendritic memb pot (mV)')
	#ax.set_box_aspect(1)
	
	
def initialize_fig_panel_i_v2(ax):
	ax.spines['right'].set_visible(False)
	ax.spines['top'].set_visible(False)
	ax.set_xlabel('Dend I (pA)')
	ax.set_box_aspect(1)
	
	
def plot_profile(filename, recs, p, i_delay):
	
	time_prerun = p['time_prerun']
	time_run    = p['time_run_after_prerun']
	dist        = p['dist']
	
	## Plot membrane potential during simulation
	height_ratios = [1,1,3,3]
	nrows = len(height_ratios)
	fig   = plt.figure(constrained_layout=True, figsize=(4.0, 8.0))
	spec  = fig.add_gridspec(ncols=1, nrows=nrows, height_ratios=height_ratios)
	axs   = [fig.add_subplot(spec[i, 0]) for i in range(nrows)]
	fig.suptitle(  'Distance from soma {} um\nT(start,Idend)- T(end,Isoma) = {} ms'.format(
                str(dist), str(i_delay)) )
	
	xmin = -50 # -time_prerun
	xmax = time_run
	
	binsize = 2
	ylabel  = '(nA)'
	
	ax = axs[0]
	ax.set_title('Current injection (dend)')
	initialize_fig_panel_profile(ax, ylabel=ylabel)
	ax.set_xlim([xmin, xmax])
	ax.set_ylim([-0.1, 1.1])
	
	ax = axs[1]
	ax.set_title('Current injection (soma)')
	initialize_fig_panel_profile(ax, ylabel=ylabel)
	ax.set_xlim([xmin, xmax])
	ax.set_ylim([-0.8, 0.2])
	
	ax = axs[2]
	ax.set_title('Membrane potential (dend)')
	initialize_fig_panel_profile(ax)
	ax.set_xlim([xmin, xmax])
	ax.set_ylim([-120, 50])
	ax.set_yticks(np.arange(-100, 40, 40))
	
	ax = axs[3]
	ax.set_title('Membrane potential (soma)')
	initialize_fig_panel_profile(ax)
	ax.set_xlim([xmin, xmax])
	ax.set_ylim([-120, 50])
	ax.set_yticks(np.arange(-100, 40, 40))
	
	cmap     = plt.get_cmap("jet")
	#cmap = plt.get_cmap("Blues")
	cmap_max = len(recs.keys())
	lw   = 0.5	
	for i, v in enumerate(recs.values()):
		#print(i)
		col = cmap( int(i) / cmap_max )
		axs[0].plot(v['t'] - time_prerun, v['i_dend'], color=col, linewidth = lw )
		axs[1].plot(v['t'] - time_prerun, v['i_soma'], color=col, linewidth = lw )
		axs[2].plot(v['t'] - time_prerun, v['v_apic'], color=col, linewidth = lw)
		axs[3].plot(v['t'] - time_prerun, v['v_soma'], color=col, linewidth = lw)
	
	
	#ax.legend(frameon=False)
	
	plt.savefig(filename + '.pdf')
	plt.savefig(filename + '.png', dpi=300)
	#plt.show()
	plt.show(block=False)
	plt.pause(2)
	plt.close()
	
	
class PlotProfiles(u.RepeatHandler):
	def __init__(self, p):
		u.RepeatHandler.__init__(self, p)
	def preprocessing_dend_amp(self):
		self.recs = {}
		self.i   = 0
		# print("self.p['i_dend_amps'][self.mode]", self.p['i_dend_amps'][self.mode])
	def function(self):
		self.recs[self.i]   = u.load(self.get_filename_simdata())
		self.i += 1
		# print('i ', self.i)
	def postprocessing_dend_amp(self):
		#pprint.pprint(self.recs)
		plot_profile(self.get_filename_fig(), self.recs, self.p, self.i_dend_delay )



def plot_i_v2(input_amp, v_apic_max, p):
	
	ctl     = p['modes'][1]
	sic_bac = p['modes'][2]
	dist     = p['dist']
	Vth      = p['Vth']
	dir_imgs = p['dir_imgs']
	dist_id  = p['dist_id']
	
	
	ctl_v_apic_max  = np.array( v_apic_max[ ctl ][0] ) # 'dend_only'
	targ_v_apic_max = v_apic_max[ sic_bac ] # 'sic'/'bac'
	i_dend = np.array(input_amp[ ctl ][0]) * 1000
	
	nrows = 1
	ncols = len( p['i_dend_delays'][sic_bac] )
	fig, axes= plt.subplots(nrows, ncols, figsize=(20.0, 2.5))
	fig.suptitle( 'Distance from soma: {:.0f} um'.format(dist) )
	
	for i, i_delay in enumerate( p['i_dend_delays'][sic_bac] ):
		ax = axes[i]
		sic_v =  np.array( targ_v_apic_max[i_delay] )
		ax.set_title(  '{:.0f} ms'.format(i_delay) )
		initialize_fig_panel_i_v2(ax)
		ax.plot( i_dend, ctl_v_apic_max,
				'o-', markersize=3, color='k', \
				markerfacecolor='w', markeredgecolor="k", markeredgewidth=1, \
				label = 'control')
		ax.plot( i_dend, sic_v,
				'o-', markersize=3, color='k', \
				markerfacecolor='k', markeredgecolor="k", markeredgewidth=1, \
				label = 'sic')
		ax.plot( [np.min(i_dend), np.max(i_dend)], [Vth, Vth], 'r-' )
		ax.set_ylim([-80, 40])
		if i == 0:
			ax.set_ylabel('Dend peak V (mV)')
		else:
			ax.axes.yaxis.set_ticklabels([])
		#ax.legend()
	
	filename =   'distid{}_i_v'.format( dist_id )
	plt.savefig(os.path.join(dir_imgs, filename + '.pdf'))
	plt.savefig(os.path.join(dir_imgs, filename + '.png'), dpi=300)
	plt.show(block=False)
	plt.pause(2)
	plt.close()


def plot_i_v(input_amp, v_apic_max, p):
	
	ctl     = p['modes'][1]
	sic_bac = p['modes'][2]
	
	ctl_v_apic_max  = np.array( v_apic_max[ ctl ][0] ) # 'dend_only'
	sics_v_apic_max = v_apic_max[ sic_bac ] # 'sic'/'bac'
	i_dend = np.array(input_amp[ ctl ][0]) * 1000
	
	dist     = p['dist']
	Vth      = p['Vth']
	dir_imgs = p['dir_imgs']
	dist_id  = p['dist_id']
	
	for i_delay in p['i_dend_delays'][sic_bac]:
	
		fig = plt.figure(constrained_layout=True, figsize=(3.0, 3.0))
		ax = fig.add_subplot()
		fig.suptitle(  'Distance from soma {} um\nT(start,Idend)- T(end,Isoma) = {} ms'.format(
                        str(dist), str(i_delay)) )
		#ax.set_title( 'T(start,Idend)- T(end,Isoma) = {} ms'.format( str(i_delay) ) )
		initialize_fig_panel_i_v(ax)		
		ax.plot( i_dend, ctl_v_apic_max,
				'o-', markersize=5, color='k', markerfacecolor='w', markeredgecolor="k", markeredgewidth=1,
				label = ctl)
		ax.plot( i_dend, np.array( sics_v_apic_max[i_delay] ),
				'o-', markersize=5, color='k', markerfacecolor='k', markeredgecolor="k", markeredgewidth=1,
				label = sic_bac)
		ax.plot( [np.min(i_dend), np.max(i_dend)], [Vth, Vth], 'r-' )
		ax.set_ylim([-80, 40])
		ax.legend()
		filename =  'distid{}_delay{}_i_v'.format( dist_id, str(i_delay).replace('-','m') )
		plt.savefig(os.path.join(dir_imgs, filename + '.pdf'))
		plt.savefig(os.path.join(dir_imgs, filename + '.png'), dpi=300)
		#plt.show()
		plt.show(block=False)
		plt.pause(2)
		plt.close()


def plot_Ith_for_V_timing_dependence(input_amp_th, p):
	
	Vth      = p['Vth']
	dist     = p['dist']
	dir_imgs = p['dir_imgs']
	dist_id  = p['dist_id']
	
	ctl      = p['modes'][1]
	sic_bac  = p['modes'][2]
	Ith_ctl  = input_amp_th[ ctl ][0] # 'dend_only'
	Ith_targ = np.array(list(input_amp_th[ sic_bac ].values()))
	delays   = np.array(list(input_amp_th[ sic_bac ].keys()))
	
	
	x_lim = [np.min(delays)*1.1, np.max(delays)*1.1]
	y_lim = [-80, 80]
	fig = plt.figure(constrained_layout=True, figsize=(5.0, 3.0))
	ax = fig.add_subplot()
	ax.spines['right'].set_visible(False)
	ax.spines['top'].set_visible(False)
	ax.set_xlabel('T(start,Idend)- T(end,Isoma) (ms)')
	ax.set_ylabel('(Ith_targ - Ith_ctl)/Ith_ctl (%)')
	ax.set_xlim(x_lim)
	ax.set_ylim(y_lim)
	fig.suptitle( 'Distance from soma: {:.0f} um, Ith: {:.0f} pA (ctl)'.format(dist, Ith_ctl) )
	
	ax.plot(x_lim,[0, 0], 'k:')
	ax.plot( delays, (Ith_targ - Ith_ctl)/Ith_ctl * 100,
				'o-', markersize=5, color='k', markerfacecolor='k', markeredgecolor="k" )
	
	filename =   'dist_{}_Ith_for_V_timing_dependence'.format( dist_id )
	plt.savefig(os.path.join(dir_imgs, filename + '.pdf'))
	plt.savefig(os.path.join(dir_imgs, filename + '.png'), dpi=300)
	plt.show(block=False)
	plt.pause(2)
	plt.close()
	

	
def plot_distance_Ih(dir_imgs, func, label):
	
	maxLength = 1300.53
	dist = np.linspace(0,maxLength,100)
	
	fig = plt.figure(constrained_layout=True, figsize=(4.0, 3.0))
	ax  = fig.add_subplot()
	ax.spines['right'].set_visible(False)
	ax.spines['top'].set_visible(False)
	ax.set_xlabel('Distance from soma (um)')
	ax.set_ylabel('gIhbar_Ih (mA/cm2)')
	
	# Control
	x3, x4, x5, x6, x7 = -0.8696, 3.6161, 0.0, 2.0870, 0.0001
	Ih  = x3 + x6*np.exp(x4*(dist/maxLength-x5))
	Ih *= x7
	
	ax.plot(dist, Ih, 'k-',label='control')
	ax.plot(dist, func(dist), 'r-',label=label)
	ax.legend()
	
	filename = 'distrib_Ih'
	plt.savefig(os.path.join(dir_imgs, filename + '.pdf'))
	plt.savefig(os.path.join(dir_imgs, filename + '.png'), dpi=300)
	plt.show(block=False)
	plt.pause(2)
	plt.close()
	
	
	

