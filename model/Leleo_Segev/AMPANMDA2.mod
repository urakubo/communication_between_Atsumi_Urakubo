TITLE AMPA and NMDA receptor with presynaptic short-term plasticity 


COMMENT
AMPA and NMDA receptor conductance using a dual-exponential profile
presynaptic short-term plasticity based on Fuhrmann et al. 2002
Implemented by Srikanth Ramaswamy, Blue Brain Project, July 2009
Etay: changed weight to be equal for NMDA and AMPA, gmax accessible in Neuron

ENDCOMMENT


NEURON {
    POINT_PROCESS AMPANMDA2  
    RANGE tau_r_AMPA, tau_d_AMPA, tau_r_NMDA, tau_d_NMDA
    RANGE Use, u, Dep, Fac, u0, weight_NMDA
    RANGE i, i_AMPA, i_NMDA, g_AMPA, g_NMDA, e, gmax
    NONSPECIFIC_CURRENT i_AMPA,i_NMDA

    POINTER rng
}

PARAMETER {
    tau_r_AMPA = 0.2  (ms) : dual-exponential conductance profile
    tau_d_AMPA = 1.7  (ms) : IMPORTANT: tau_r < tau_d
    tau_r_NMDA = 0.29 (ms) : dual-exponential conductance profile
    tau_d_NMDA = 43   (ms) : IMPORTANT: tau_r < tau_d
    e          = 0    (mV) : AMPA and NMDA reversal potential
    mg         = 1    (mM) : initial concentration of mg2+
    mggate
    gmax       = .001 (uS) : weight conversion factor (from nS to uS)
}

COMMENT
The Verbatim block is needed to generate random nos. from a uniform distribution between 0 and 1 
for comparison with Pr to decide whether to activate the synapse or not
ENDCOMMENT


ASSIGNED {

        v (mV)
        i (nA)
	i_AMPA (nA)
	i_NMDA (nA)
   g_AMPA (uS)
	g_NMDA (uS)
   factor_AMPA
	factor_NMDA
	rng
	weight_NMDA
}

STATE {
    A_AMPA       : AMPA state variable to construct the dual-exponential profile - decays with conductance tau_r_AMPA
    B_AMPA       : AMPA state variable to construct the dual-exponential profile - decays with conductance tau_d_AMPA
    A_NMDA       : NMDA state variable to construct the dual-exponential profile - decays with conductance tau_r_NMDA
    B_NMDA       : NMDA state variable to construct the dual-exponential profile - decays with conductance tau_d_NMDA
}

INITIAL{
    LOCAL tp_AMPA, tp_NMDA
        
	 A_AMPA = 0
    B_AMPA = 0
	
	 A_NMDA = 0
	 B_NMDA = 0
        
	 tp_AMPA = (tau_r_AMPA*tau_d_AMPA)/(tau_d_AMPA-tau_r_AMPA)*log(tau_d_AMPA/tau_r_AMPA) :time to peak of the conductance
	 tp_NMDA = (tau_r_NMDA*tau_d_NMDA)/(tau_d_NMDA-tau_r_NMDA)*log(tau_d_NMDA/tau_r_NMDA) :time to peak of the conductance
        
	 factor_AMPA = -exp(-tp_AMPA/tau_r_AMPA)+exp(-tp_AMPA/tau_d_AMPA) :AMPA Normalization factor - so that when t = tp_AMPA, gsyn = gpeak
    factor_AMPA = 1/factor_AMPA
	
	 factor_NMDA = -exp(-tp_NMDA/tau_r_NMDA)+exp(-tp_NMDA/tau_d_NMDA) :NMDA Normalization factor - so that when t = tp_NMDA, gsyn = gpeak
    factor_NMDA = 1/factor_NMDA
}

BREAKPOINT {
    SOLVE state METHOD cnexp
   
    mggate = 1 / (1 + exp(0.08  (/mV) * -(v)) * (mg / 3.57 (mM))) :mggate kinetics - Jahr & Stevens 1990
    g_AMPA = gmax*(B_AMPA-A_AMPA)            :compute time varying conductance as the difference of state variables B_AMPA and A_AMPA
    g_NMDA = gmax*(B_NMDA-A_NMDA) * mggate   :compute time varying conductance as the difference of state variables B_NMDA and A_NMDA and mggate kinetics
    i_AMPA = g_AMPA*(v-e)                    :compute the AMPA driving force based on the time varying conductance, membrane potential, and AMPA reversal
    i_NMDA = g_NMDA*(v-e)                    :compute the NMDA driving force based on the time varying conductance, membrane potential, and NMDA reversal
    i = i_AMPA + i_NMDA
}

DERIVATIVE state{
    A_AMPA' = -A_AMPA/tau_r_AMPA
    B_AMPA' = -B_AMPA/tau_d_AMPA
    A_NMDA' = -A_NMDA/tau_r_NMDA
    B_NMDA' = -B_NMDA/tau_d_NMDA
}


NET_RECEIVE (weight,weight_AMPA, weight_NMDA, Pv, Pr, u, tsyn (ms)){
    weight_AMPA = weight
    weight_NMDA = weight
    A_AMPA = A_AMPA + weight_AMPA*factor_AMPA
    B_AMPA = B_AMPA + weight_AMPA*factor_AMPA
    A_NMDA = A_NMDA + weight_NMDA*factor_NMDA
    B_NMDA = B_NMDA + weight_NMDA*factor_NMDA
}
