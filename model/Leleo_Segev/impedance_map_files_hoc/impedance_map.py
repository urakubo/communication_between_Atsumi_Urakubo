from neuron import h,gui
import math
import numpy as np
h('load_file("nrngui.hoc")')

h('xopen("$(NEURONHOME)/lib/hoc/noload.hoc")')
h('load_proc("nrnmainmenu")')

h('xopen("Neuron_parameters.hoc")')

h.geom_nseg()
h.parameters()
h.drug()
h.init_channels()

IMP_FREQ = 0

MIN_Z_in = math.log(50)
MAX_Z_in = math.log(60000)


MIN_Z_tr = math.log(1)
MAX_Z_tr = math.log(70)

LOG_SCALE = 1

for sec in h.all:
    sec.insert("var")

h.cvode_active(0)

imp = h.Impedance()
imp.loc(0.5,sec=h.soma)
imp.compute(IMP_FREQ,0)
MIN_Z = 1000
MAX_Z = 0
for sec in h.all:
	for seg in sec:
		if LOG_SCALE:
			seg.zin_var =math.log(imp.input(seg.x,sec=sec))
			seg.ztr_var =math.log(imp.transfer(seg.x,sec=sec))
		else:
			seg.zin_var = imp.input(seg.x,sec=sec)
			seg.ztr_var = imp.transfer(seg.x,sec=sec)

		



h('load_file("TColorMap.hoc")')

ps_i =  h.PlotShape()
ps_i.exec_menu("View = plot")
ps_i.variable("zin_var")
cm1 = h.TColorMap("cm/jet.cm")
cm1.set_color_map(ps_i,MIN_Z_in,MAX_Z_in)
h.fast_flush_list.append(ps_i)
ps_i.exec_menu("Shape Plot")
ps_i.exec_menu("Variable Scale")
# Un tag in the human model:
# ps_i.rotate(0,0,0,0,0,1.6)


ps_t =  h.PlotShape()
ps_t.exec_menu("View = plot")
ps_t.variable("ztr_var")
cm1 = h.TColorMap("cm/jet.cm")
cm1.set_color_map(ps_t,MIN_Z_tr,MAX_Z_tr)
h.fast_flush_list.append(ps_t)
ps_t.exec_menu("Shape Plot")
ps_t.exec_menu("Variable Scale")

# Un tag in the human model:
# ps_t.rotate(0,0,0,0,0,1.6)

