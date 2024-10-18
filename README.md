![System requirements](https://img.shields.io/badge/python-3.8-red.svg)
![System requirements](https://img.shields.io/badge/platform-win%2064,%20linux%2064-green.svg)
[![License: GPL v3](https://img.shields.io/badge/license-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

# Simulation code for "Somatic inhibition-Induced Ca2+ spike (SIC)"

The GitHub repository contains analysis programs for the study "XXXX" by Atsumi et al. [1].
All programs were written in Python3.8 (Windows/Linux) and designed for the simulation on the NEURON simulator [2].

[1] XXXX

[2] https://neuron.yale.edu/neuron/

## Basic procedure

Simulation and analyses are conducted on the basement directory. Executable programs refers utility programs in the src directory and NEURON models in the model directory.

#### Directories
| directory | contents |
| -------- | -------- |
| **`src`** |Executable Python programs |
| **`model`**| Neuron models |
| **`x86_64`**| NEURON simulation complied for the neuron models (linux) |

#### .py files to check when starting a simulation

| .py file | functions |
| -------- | -------- |
| **`main_current.py`** | It simulates SIC, BAC, and the SIC during local application of TTX to the soma. |
| **`configuration.py`** | It defines basic parameters. It also produces a series of the dict variable required for each run. The dict varible is read by  |
| **`main_check_channel_distribution.py`**| It visualizes the Na and Cation channel distribution. |

"main_current.py" calls the function "create_simulation" located in "src/model_simulation.py". It accepts the following dict variable, builds a neuron model, run a simulation, and save a simulation result.


| key | value type | description |
| -------- | -------- | -------- |
| **`apply_soma_ttx`** | bool | True or False. |
| **`filename`** | str | directory and filename to store simulation results. |
| **`i_dend_amp`** | float | Amplitude of dendritic current injection (nA). |
| **`i_dend_delay`** | float | Onset time of dendritic current injection after prerun (ms). |
| **`i_dend_sec_id`** | float | Section id (L5PC.apic[X]) of current injection site at the apical trunk. |
| **`i_dend_seg`** | float | Segment of the apical trunk. |
| **`i_soma_amp`** | float | Amplitude of somatic current injection (nA). |
| **`i_soma_duration`** | float | Duration of somatic current injection (nA). |
| **`time_onset_for_v_peak_detection_after_prerun`** | float | Onset time for the detection of peak v (ms). |
| **`time_prerun`** | float | Prerun time (ms). |
| **`time_run_after_prerun`** | float | Simulation time after the prerun (ms). |
| **`Vth`** | int | Threshold amplitude of membrane potential to determine it as a spike. |


