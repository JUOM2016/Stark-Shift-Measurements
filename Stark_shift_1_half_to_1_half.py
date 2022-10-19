import zhinst.utils as zu
import numpy as np
from scipy.signal import chirp
from measurements.libs.QPLser.AWGmanager import HDAWG_PLser

###  Initiliase HDAWG system  ###
device = 'dev8416'  # device ID for G14.
awgMod = HDAWG_PLser(device)
command_table = 1

## Common Parameter Definition
# Clock Parameters
sampling_rate=2.4E9 # Hz; Sampling rate, should be the same as what you set on the right panel!

# Burning Pulse Parameters
Number_of_burning_pulses = 299 # Number of burning pulse repetitions  
centre_freq_burning=250E6 #Hz; Central frequency set to drive the AOM for burning 
chirpAmplitude_burning = 0.1 # V; amplitude of burning pulse 
freq_sweeping_burning=3E6 # Hz; set the scanning frequency range of burning pulse (the actual scanning range should be 4*freq_detuning)
burning_duration=0.6E-3 #s; burning time 
burning_samples = round(burning_duration*sampling_rate/16)*16 # Calculating sampling points 
burning_t = np.linspace(0,burning_duration,burning_samples)

# Burning Back Pulse Parameters
Number_of_burning_back_pulses = 300 # Number of burn-back pulse repetitions 
centre_freq_burning_back=268.45E6 # Hz; Central frequency set to drive the AOM for burn-back
chirpAmplitude_burning_back = 0.035# V; amplitude of burn-back
freq_sweeping_burning_back=0 #Hz; set the scanning frequency range of burn-back (the actual scanning range should be 4*freq_detuning)
burning_back_duration=0.05E-3 #s; burning time burn-back
burning_back_samples = round(burning_back_duration*sampling_rate/16)*16 # Calculating sampling points 
burning_back_t = np.linspace(0,burning_back_duration,burning_back_samples)

# Reading Pulse Parameters
centre_freq_reading=250E6 # Hz; Central frequency set to read out the burned spectral hole
chirpAmplitude_reading = 0.03 # V; amplitude of reading-out pulse
freq_sweeping_reading=2E6 # Hz; set the scanning frequency range of reading-out pulse (the actual scanning range should be 4*freq_detuning) 1.32877326E6
reading_duration=4e-3 # s; reading-out time
reading_samples = round(reading_duration*sampling_rate/16)*16 # Calculating sampling points 
reading_t = np.linspace(0,reading_duration,reading_samples)

# Stark Shift Field Parameters
Number_of_amplitudes = 10 # Number of amplitues for stark shift measurements
rect_amplitude = 1 # V; amplitude of rectangular pulse train
# rect_t = np.linspace(0,reading_duration,reading_samples)

# Shuffle Pulse Parameters
centre_freq_shuffle=250E6 # Hz; Central frequency of the shuffle pulse
chirpAmplitude_shuffle = 0.21 # V; amplitude of shuffling pulse
freq_sweeping_shuffle=20E6 # Hz; set the scanning frequency range of shuffling pulse
shuffle_duration=100e-6 # s; shuffling time
shuffle_samples = round(shuffle_duration*sampling_rate/16)*16 # Calculating sampling points 
shuffle_t = np.linspace(0,shuffle_duration,shuffle_samples)

## Waveform Definition

wave_burning = chirpAmplitude_burning*chirp(burning_t,centre_freq_burning-freq_sweeping_burning/2,burning_duration,centre_freq_burning+freq_sweeping_burning/2)

wave_burning_back = chirpAmplitude_burning_back*chirp(burning_back_t,centre_freq_burning_back-freq_sweeping_burning_back/2,burning_back_duration,centre_freq_burning_back+freq_sweeping_burning_back/2)

wave_reading = chirpAmplitude_reading*chirp(reading_t,centre_freq_reading-freq_sweeping_reading/2,reading_duration,centre_freq_reading+freq_sweeping_reading/2)

wave_rect = rect_amplitude*np.ones(reading_samples)

wave_shuffle = chirpAmplitude_shuffle*chirp(shuffle_t,centre_freq_shuffle-freq_sweeping_shuffle/2,shuffle_duration,centre_freq_shuffle+freq_sweeping_shuffle/2)

## Create Command Table ## 

if command_table==1:
    # Save Location 
    # save_directory ='C:/Codes/measurements/libs/QPLser/ZI_HDAWG_Scripts/Command_Tables/'
    save_directory = 'C:/Users/fdg2/Documents/HDAWG Pulse Sequences/Stark Shift Measurements/'

    # file name
    file_name= 'CT_Stark_shift_1_half_to_1_half'
    # Open the file
    f = open(os.path.join(save_directory+ file_name), 'w')
    # Write the basic intro of the file
    f.write('{' + '\n' + '  '
        '"$schema": "http://docs.zhinst.com/hdawg/commandtable/v2/schema",' + '\n' + '  '
        '"header": {' + '\n' + '\t' + '"version": "0.2",' + '\n' + '\t' 
        '"UserString": "' + file_name + '",' + '\n' + '\t'  + '"partial": true,' + '\n' + '\t'  + '"description": "Command table for Stark shift measurements"' +  '\n' + '  },' + '\n'
        '  "table": [' + '\n')
    # Write the index assigning
    a=np.arange(0,Number_of_amplitudes)
    b=np.linspace(0,rect_amplitude,Number_of_amplitudes)
    for i in range(0, len(a)): 
        f.write('\t'+'{' + '\n'
                + '\t' + '"index": '+str( i)+',' + '\n'
                + '\t' + '  "waveform": {' + '\n'
                + '\t' + '\t'  +  '  "index": '+str( 10) + '\n'
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
HDAWG_filename = ('C:\Codes\HDAWG\Sequences\Stark_shift_1_half_to_1_half.txt')

with open(HDAWG_filename, "r") as file:
    awg_string = file.read()
    awg_program = awg_string.format(

        # Clock Parameters
        sampling_rate=sampling_rate, # Hz; Sampling rate, should be the same as what you set on the right panel!
        
        # Burning Parameters
        Number_of_burning_pulses =Number_of_burning_pulses,
        burning_duration=burning_duration, #s; burning time  

        # Burning Back Parameters
        Number_of_burning_back_pulses =Number_of_burning_back_pulses,
        burning_back_duration=burning_back_duration, #s; burning time burn-back
        
        # Reading Parameters
        reading_duration=reading_duration, # s; reading pulse duration

        # Shuffle Parameters
        shuffle_duration=shuffle_duration #s; shuffling time
        )
    
awgMod.compile(device, awg_program)

# Convert and send to the HDAWG

chirpedSine_burning = zu.convert_awg_waveform(wave_burning)
chirpedSine_burning_back = zu.convert_awg_waveform(wave_burning_back)
chirpedSine_reading = zu.convert_awg_waveform(wave_reading)
w_flat = zu.convert_awg_waveform(wave_rect, wave_rect)
chirpedSine_shuffle = zu.convert_awg_waveform(wave_shuffle)

set_cmd = [(f'/{device}/awgs/0/waveform/waves/1', chirpedSine_burning),
           (f'/{device}/awgs/0/waveform/waves/2', chirpedSine_burning_back),
           (f'/{device}/awgs/0/waveform/waves/3', chirpedSine_shuffle),
           (f'/{device}/awgs/0/waveform/waves/10', chirpedSine_reading),
           (f'/{device}/awgs/1/waveform/waves/10', w_flat)]

awgMod.daq.set(set_cmd)

### Set HDAWG parameters/settings ###

awgMod.set_value(f"/{device}/sines/0/enables/0", 0)

awgMod.set_value(f"/{device}/triggers/out/0/source", 4) # set up trigger, Output 1 Marker 1

## setup output channels 
awgMod.set_value(f"/{device}/sigouts/0/on", 1) # Channel 1 is ON
awgMod.set_value(f"/{device}/sigouts/1/on", 0)
awgMod.set_value(f"/{device}/sigouts/2/on", 1)
awgMod.set_value(f"/{device}/sigouts/3/on", 1)

awgMod.set_value(f"/{device}/awgs/0/single",0) # Rerun sequence