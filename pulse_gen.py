import numpy as np
import pandas as pd
import os

def generate_waveform(frequency, height1, height2, time_diff, pulse_width1, pulse_width2,offset):
    period = 1 / frequency  # Period in seconds
    total_time = period * 1e6  # Convert to microseconds
    
    sample_rate = 5 / 0.001  # 1 sample per 0.001 microsecond (1/1000 ns)
    time_array = np.arange(0, total_time, 1/sample_rate)  # Time in microseconds
    waveform = np.full_like(time_array, offset)
    
    pulse_start1 = 0
    pulse_end1 = pulse_start1 + (pulse_width1 / 1000)  # Convert ns to microseconds
    pulse_start2 = pulse_end1 + time_diff
    pulse_end2 = pulse_start2 + (pulse_width2 / 1000)  # Convert ns to microseconds

    # Generate first pulse
    waveform[(time_array >= pulse_start1) & (time_array < pulse_end1)] = height1 + offset
    # Generate second pulse
    waveform[(time_array >= pulse_start2) & (time_array < pulse_end2)] = height2 + offset
    
    return time_array, waveform

# Get user input
frequency = float(input("Enter pulse frequency (in Hz): "))
height1 = float(input("Enter first pulse height (in V): "))
height2 = float(input("Enter second pulse height (in V): "))
time_diff = float(input("Enter time difference between two pulses (in us): "))
offset = 0.9
amp = 3
dlength = int(1e9 / frequency)

# Get pulse widths with default values
pulse_width1 = input("Enter first pulse width (default 100 ns, press enter to keep default): ")
if pulse_width1 == "":
    pulse_width1 = 100  # Default in nanoseconds
else:
    pulse_width1 = float(pulse_width1)

pulse_width2 = input("Enter second pulse width (default 1 us, press enter to keep default): ")
if pulse_width2 == "":
    pulse_width2 = 1000  # Default in nanoseconds
else:
    pulse_width2 = float(pulse_width2)

# Generate waveform
time_array, waveform = generate_waveform(frequency, height1, height2, time_diff, pulse_width1, pulse_width2, offset)

# Prepare header information
header = [
    f"data length,{dlength}",
    f"frequency,{frequency:.6f}",
    f"amp,{amp:.1f}",
    f"offset,{offset:.1f}",
    "phase,0.000000",
    "",
    "",
    "",
    "",
    "",
    "",
]

# Prepare DataFrame with integer xpos and waveform values
xpos = np.arange(len(time_array))
waveform_data = pd.DataFrame({'xpos': xpos, 'value': waveform})

# Create filename
filename = f"waveform_{frequency}Hz_{height1}V_{height2}V_{time_diff}us_{pulse_width1}ns_{pulse_width2}us.csv"

# Save to CSV with header
with open(filename, 'w') as f:
    for line in header:
        f.write(line + '\n')
    waveform_data.to_csv(f, index=False)

print(f"Waveform data saved to {filename}")
