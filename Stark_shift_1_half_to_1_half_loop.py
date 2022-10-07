from measurements.libs.QPLser.AWGmanager import HDAWG_PLser
import numpy as np
import os

###  Initiliase HDAWG system  ###
device = 'dev8416'  # device ID for G14.
awgMod = HDAWG_PLser(device)
command_table=1

sampling_rate=2.4E9 # Hz; Sampling rate, should be the same as what you set on the right panel!


## HDAWG parameters for pulse sequency
Number_of_burning_pulses = 299 # Number of burning pulse repetitions  
Number_of_burning_back_pulses = 200 # Number of burn-back pulse repetitions 
Number_of_amplitudes = 5 # Number of stark shift amplitudes
Number_of_stark_readings = 10 # Number of averages for Stark measurements

centre_freq_burning=250E6 #Hz; Central frequency set to drive the AOM for burning 
chirpAmplitude_burning = 0.1 # V; amplitude of burning pulse 
freq_sweeping_burning=3E6 # Hz; set the scanning frequency range of burning pulse (the actual scanning range should be 4*freq_detuning)
burning_duration=0.6E-3 #s; burning time 

centre_freq_burning_back=268.45E6 # Hz; Central frequency set to drive the AOM for burn-back
chirpAmplitude_burning_back = 0.025 # V; amplitude of burn-back
freq_sweeping_burning_back=0 #Hz; set the scanning frequency range of burn-back (the actual scanning range should be 4*freq_detuning)
burning_back_duration=0.1E-3 #s; burning time burn-back

centre_freq_reading=250E6 # Hz; Central frequency set to read out the burned spectral hole
chirpAmplitude_reading = 0.03 # V; amplitude of reading-out pulse
freq_sweeping_reading=2E6 # Hz; set the scanning frequency range of reading-out pulse (the actual scanning range should be 4*freq_detuning) 1.32877326E6
reading_duration=4e-3 # s; reading-out time

rect_amplitude = 1 # V; amplitude of rectangular pulse train

centre_freq_shuffle=250E6#Hz; Central frequency of the shuffle pulse
chirpAmplitude_shuffle = 0.21 # V; amplitude of shuffling pulse
freq_sweeping_shuffle=20E6 #Hz; set the scanning frequency range of shuffling pulse
shuffle_duration=100e-6 #s; shuffling time

## Create Command Table ## 

if command_table==1:
    # Save Location 
    save_directory ='C:/Codes/measurements/libs/QPLser/ZI_HDAWG_Scripts/Command_Tables/'
    # save_directory = 'C:/Users/fdg2/Documents/Simulation/Optimal AFC Preperation/'

    # file name
    file_name= 'CT_Stark_shift_1_half_to_1_half_loop'
    # Open the file
    f = open(os.path.join(save_directory+ file_name), 'w')
    # Write the basic intro of the file
    f.write('{' + '\n' + '  '
        '"$schema": "http://docs.zhinst.com/hdawg/commandtable/v2/schema",' + '\n' + '  '
        '"header": {' + '\n' + '\t' + '"version": "0.2",' + '\n' + '\t' 
        '"UserString": "' + file_name + '",' + '\n' + '\t'  + '"partial": true,' + '\n' + '\t'  + '"description": "Command table for optimal AFC preperation"' +  '\n' + '  },' + '\n'
        '  "table": [' + '\n')
    # Write the index assigning
    a=np.arange(0,Number_of_amplitudes)
    b=np.linspace(0,rect_amplitude,Number_of_amplitudes)
    for i in range(0, len(a)): 
        f.write('\t'+'{' + '\n'
                + '\t' + '"index": '+str( i)+',' + '\n'
                + '\t' + '  "waveform": {' + '\n'
                + '\t' + '\t'  +  '  "index": '+str( 0) + '\n'
                + '\t' + '  },' + '\n'
                + '\t' + '  "amplitude1": {' + '\n'
                + '\t' + '\t'  +   '"value": ' + str( b[i]) + '\n'
                + '\t' + '}' + '\n'
                )
        if i==len(a)-1:
            f.write('\t' + '}' + '\n')
        else:
            f.write('\t' + '},' + '\n')
# end parenthesis
    f.write('  ]' + '\n' + '}')
# close the file
    f.close()

## Load correct Sequence file
HDAWG_filename = ('C:\Codes\HDAWG\Sequences\Stark_shift_1_half_to_1_half_loop.txt')

with open(HDAWG_filename, "r") as file:
    awg_string = file.read()
    awg_program = awg_string.format(
        sampling_rate=sampling_rate, # Hz; Sampling rate, should be the same as what you set on the right panel!
        Number_of_burning_pulses =Number_of_burning_pulses,
        Number_of_burning_back_pulses =Number_of_burning_back_pulses,
        centre_freq_burning=centre_freq_burning, #Hz; Central frequency set to drive the AOM for burning 
        chirpAmplitude_burning=chirpAmplitude_burning, # V; amplitude of burning pulse 
        freq_sweeping_burning=freq_sweeping_burning, # Hz; set the scanning frequency range of burning pulse (the actual scanning range should be 4*freq_detuning)
        burning_duration=burning_duration, #s; burning time  
        centre_freq_burning_back=centre_freq_burning_back, # Hz; Central frequency set to drive the AOM for burn-back  
        chirpAmplitude_burning_back = chirpAmplitude_burning_back, # V; amplitude of burn-back
        freq_sweeping_burning_back=freq_sweeping_burning_back, #Hz; set the scanning frequency range of burn-back (the actual scanning range should be 4*freq_detuning)
        burning_back_duration=burning_back_duration, #s; burning time burn-back
        centre_freq_reading=centre_freq_reading, #Hz; Central frequency set to read out the burned spectral hole
        chirpAmplitude_reading = chirpAmplitude_reading, # V; amplitude of reading-out pulse
        freq_sweeping_reading=freq_sweeping_reading, # Hz; set the scanning frequency range of reading-out pulse (the actual scanning range should be 4*freq_detuning) 1.32877326E6
        reading_duration=reading_duration,
        centre_freq_shuffle=centre_freq_shuffle, #Hz; Central frequency of the shuffle pulse
        chirpAmplitude_shuffle = chirpAmplitude_shuffle,# V; amplitude of shuffling pulse
        freq_sweeping_shuffle=freq_sweeping_shuffle, #Hz; set the scanning frequency range of shuffling pulse
        shuffle_duration=shuffle_duration, #s; shuffling time
        rect_amplitude=rect_amplitude,
        Number_of_amplitudes=Number_of_amplitudes,
        Number_of_stark_readings=Number_of_stark_readings
        )
    
awgMod.compile(device, awg_program)
awgMod.upload_command_table(device, command_table='CT_Stark_shift_1_half_to_1_half_loop')

### Set HDAWG parameters/settings ###

awgMod.set_value(f"/{device}/sines/0/enables/0", 0)

awgMod.set_value(f"/{device}/triggers/out/0/source", 4) # set up trigger, Output 1 Marker 1

## setup output channels 
awgMod.set_value(f"/{device}/sigouts/0/on", 1) # Channel 1 is ON
awgMod.set_value(f"/{device}/sigouts/1/on", 1)
awgMod.set_value(f"/{device}/sigouts/2/on", 0)
awgMod.set_value(f"/{device}/sigouts/3/on", 0)

awgMod.set_value(f"/{device}/awgs/0/single",0) #Rerun sequence