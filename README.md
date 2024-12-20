![System requirements](https://img.shields.io/badge/python-3.8-red.svg)
![System requirements](https://img.shields.io/badge/platform-win%2064,%20linux%2064-green.svg)
[![License: GPL v3](https://img.shields.io/badge/license-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

# Communication between Atsumi and Urakubo

<!--
Simulation code for "Somatic inhibition-Induced Ca2+ spike (SIC)"
-->


The GitHub repository contains simulation and analysis programs for the study "XXXX" by Atsumi et al. [1].
All programs are written in Python3.8 (Windows/Linux) and designed for the simulation on the NEURON simulator [2].

[1] XXXX

[2] https://neuron.yale.edu/neuron/

## Basic procedure

Simulation and analyses are conducted on the base directory. Executable programs (main_xxx.py files) refers to utility programs in the src directory and NEURON models in the model directory.


#### .py files to check when starting a simulation
| .py file | functions |
| -------- | -------- |
| **`main_current.py`** | It simulates SIC, BAC, and the SIC during local application of TTX to the soma. It also simulate them under altered distribution of h channels. |
| **`main_plot_summary.py`** | It creates summary figures. WIP. |
| **`main_check_channel_distribution_Na.py`**| It visualizes Na channel distribution. It was used to make a mimic of TTX application to the soma. |
| **`main_check_channel_distribution_h.py`**| It visualizes h channel distribution (graph and image). It was used to create altered distribution of h channels. |
| **`main_check_loc_distance.py`**| It was used to determine current injection sites along the apical trunk. |
| **`configuration.py`** | It defines parameters. It also produces a series of the dict variable required for each run. The dict variable is read by the function "src.model_simulation.create_simulation". |


#### Directories
| directory | contents |
| -------- | -------- |
| **`src`** |Executable programs of Python |
| **`model`**| Neuron models |
| **`x86_64`**| NEURON simulation complied for the neuron models (linux) |


"main_current.py" calls the function "create_simulation" located in "src/model_simulation.py". The "create_simulation"  function accepts the following dict variable, builds a model neuron, run simulation, and save simulation results.


#### Dict variable for the input argument of "src.model_simulation.create_simulation"
| key | value type | description |
| -------- | -------- | -------- |
| **`apply_soma_ttx`** | bool | True or False. |
| **`filename`** | str | Directory and filename to store simulation results. |
| **`i_dend_amp`** | float | Amplitude of dendritic current injection (nA). |
| **`i_dend_delay`** | float | Onset time of dendritic current injection after i_soma (ms). |
| **`i_dend_sec_id`** | int | Section id (L5PC.apic[X]) of current injection site at the apical trunk. |
| **`i_dend_seg`** | float | Segment of the apical trunk. |
| **`i_soma_amp`** | float | Amplitude of somatic current injection (nA). |
| **`i_soma_duration`** | float | Duration of somatic current injection (nA). |
| **`time_onset_for_v_peak_detection`** | float | Onset time for the detection of peak v (ms). |
| **`time_prerun`** | float | Prerun time (ms). |
| **`time_run_after_prerun`** | float | Simulation time after the prerun (ms). |
| **`time_set_zero`** | float | Simulation time set to zero in the graph (ms). |
| **`Vth`** | float | Threshold amplitude of membrane potential to determine it as a spike (mV). |
| **`distrib_h`** | str | Optional. 'reverse','uniform',or 'none' distribution of h channels.|



## Input and output of the function "configuration.set_params"

The function "configuration.set_params" is the loader of simulation parameters.


#### Input variables
| key | value type | description |
| -------- | -------- | -------- |
| **`mode`** | str | 'sic', 'ttx', or 'bac'. |
| **`dist_id`** | int | IDs of dendritic location. 0 ,..., 11. |



#### Output dict variable
| key | value type | description |
| -------- | -------- | -------- |
| **`mode`** | str | 'sic', 'ttx', or 'bac'. |
| **`dists`** | list(float) | List of distances (um) of dendritic input sites. |
| **`i_dend_sec_ids`** | list(int) | List of sections of dendritic input sites. |
| **`i_dend_segs`** | list(float) | List of segments of dendritic input sites. |
| **`dist_id`** | int | ID of target input site of dendrite. |
| **`dist`** | float | Distance (um) of target input site of dendrite from the soma. |
| **`i_dend_sec_id`** | float | Section of target input site of dendrite. |
| **`i_dend_seg`** | float | Segment of target input site of dendrite. |
| **`Vth`** | float | Voltage threshold for dendritic spiking (mV). |
| **`dir_data`** | str | Directory for data files. |
| **`dir_imgs`** | str | Directory for images. |
| **`dir_imgs_summary`** | str | Directory for summary images. |
| **`stim_types`** | list(str) | 'soma_only', 'dend_only', or 'soma_and_dend' |
| **`i_dend_delays`** | dict(list(float)) | Delays of onset of dendritic current (ms, list) for each of stim_types (dict key). |
| **`i_dend_amps`** | dict(list(float)) | Amplitudes of dendritic current (nA, list) for each of stim_types (dict key). |
| **`i_soma_amps`** | dict(float) | Amplitude of somatic current (nA) for each of stim_types (dict key).|
| **`i_soma_duration`** | float | Duration of somatic current (ms).|
| **`apply_soma_ttx`** | bool | True or False of TTX application.|
| **`distrib_h`** | str | Optional. 'reverse','uniform',or 'none' distribution of h channels.|



## Outputs from the run of src.utils.I_V
#### input_amp
| key | value type | description |
| -------- | -------- | -------- |
| **`soma_only`** | dict(list(float)) | {0: \[0\]} . Amplitude of dendritic current (0 nA) for the delay 0 ms. |
| **`dend_only`** | dict(list(float)) | {0: \[I<sub>0</sub>, ..., I<sub>n</sub>\]} . One element dict (key: 0 ms). Amplitudes of dendritic current (nA, list) the delay 0 ms. |
| **`soma_and_dend`** | dict(list(float)) | {-80: \[I<sub>0</sub>, ..., I<sub>n</sub>\],...,80: \[I<sub>0</sub>, ..., I<sub>n</sub>\]} . Amplitudes of dendritic current (nA, list) for each delay (ms, dict key). |


#### v_apic_max
| key | value type | description |
| -------- | -------- | -------- |
| **`soma_only`** | dict(list(float)) | {0: \[X\]} . Maximal dendritic V (mV) for the delay 0 ms. |
| **`dend_only`** | dict(list(float)) | {0: \[V<sub>0</sub>, ..., V<sub>n</sub>\]} . One element dict (key: 0 ms). Maximal dendritic V (mV, list) for the delay 0 ms. |
| **`soma_and_dend`** | dict(list(float)) | {-80: \[V<sub>-80,0</sub>, ..., V<sub>-80,n</sub>\],...,80: \[V<sub>80,0</sub>, ..., V<sub>80,n</sub>\]} Maximal dendritic V (mV, list) for each delay (ms, dict). |


#### input_amp_th
| key | value type | description |
| -------- | -------- | -------- |
| **`soma_only`** | dict(float) | {0: None} . |
| **`dend_only`** | dict(float) | {0: I<sub>th</sub>} . One element dict (key: 0 ms). I_threshold for spike (nA, dict value) for the delay 0 (ms, dict key). |
| **`soma_and_dend`** | dict(float) | {-80: I<sub>-80,th</sub>, ..., 80: I<sub>80,th</sub>} . I_threshold for spike (nA, dict value)  for each delay (ms, dict key). |


## NEURONモデルを変えたい場合
既定で、[**Leleo & Segev (2021, PLoS Comput Biol)**](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1009558) のモデルを採用しています。 [**Shai , ..., Koch (2015, PLoS Comput Biol)**](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1004090) モデルも実行可能です。src.model_simulation.create_cell 関数の指定部分を入れ替えるとモデルが変更されます。これら二つのモデルはhチャネル分布を除きほぼ同一と思われますが、mod のパラメータ (h チャネルのkinetics 等) が変更されているかも知れず、その場合はコンパイル後NEURONも差し替える必要があります。また、BAC実験のために発火に必要な最小の電流や、hチャネルのreverse, uniform, none 分布などは、別に設定／計算しなおす必要があります。
