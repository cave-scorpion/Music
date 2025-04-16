"""
This script will read a directory of sample WAV files and create a new directory called "directory"_RMS filled with the samples sorted by RMS value.
Samples must be WAV files. If there are errors with the file types, it may be due to low bit rate. Testing has found issues with bit rates < 1000 kbps.
"""

import subprocess, sys, wave, os, shutil

try:
    import numpy as np
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", 'numpy'])
finally:
    import numpy as np
    
path = "E:/IMPORT/Drums - One Shots/" ## Change this to be one directory above your sample folder
sample_folder = "Kicks" ## Name of your sample folder

def calculate_rms(file_path):
    """Return RMS of a mono WAV file."""
    with wave.open(file_path, 'rb') as wav_file:
        samples = wav_file.getnframes()
        audio_data = wav_file.readframes(samples)
        # Convert the audio data to a NumPy array
        audio_array = np.frombuffer(audio_data, dtype=np.int16) / 2 ** 15
        return np.sqrt(np.mean(np.square(audio_array)))

sample_list = {}
for sample in sorted(os.listdir(path+sample_folder+"/")):
    #print(sample)
    rms_value = calculate_rms(path+sample_folder+"/"+sample)
    #print(sample, f'RMS value: {rms_value} linear, {20 * np.log10(rms_value)} dB.')
    new_entry = {sample: rms_value}
    sample_list.update(new_entry)

sample_list_sorted = sorted(sample_list.items(), key=lambda x:x[1], reverse = True)

if not os.path.exists(path+"/"+sample_folder+"_RMS"):
   os.makedirs(path+"/"+sample_folder+"_RMS")

for samples in range(len(sample_list_sorted)):
    shutil.copy(path+sample_folder+"/"+sample_list_sorted[samples][0], path+"/"+sample_folder+"_RMS/"+str(samples+1)+'-'+sample_list_sorted[samples][0])

print('Sorted directory: '+path+sample_folder+"_RMS")