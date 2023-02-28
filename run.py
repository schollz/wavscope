import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from icecream import ic

## waveform viz
from os.path import dirname, join as pjoin
from scipy.io import wavfile
import scipy.io

data_dir = pjoin(dirname(scipy.io.__file__), "tests", "data")
wave_filename = pjoin(data_dir, "test-44100Hz-2ch-32bit-float-be.wav")
wave_samplerate, data = wavfile.read(wave_filename)
wave_num_channels = data.shape[1]
wave_duration = data.shape[0] / wave_samplerate
ic(wave_filename, wave_samplerate, wave_num_channels, wave_duration)
import matplotlib.pyplot as plt
import numpy as np

wave_samples = np.arange(0, data.shape[0])
wave_time = wave_samples / wave_samplerate
wave_data = data[:, 0]
last = 0
wave_crossings = []
for i, v in enumerate(wave_data):
    if np.sign(v) == 0:
        continue
    if np.sign(v) != last:
        wave_crossings.append(i)
    last = np.sign(v)
ic(wave_crossings)
ind = np.where(np.logical_and(wave_time >= 0.003, wave_time <= 0.005))
ic(ind)
future_crossings = np.where(wave_crossings > ind[0][0])[0]
ic(wave_crossings[future_crossings[0]])
target_freq = 440

for i, v in enumerate(future_crossings):
    if i > 0:
        # TODO: find next crossing that is closest to specified freq
        ic(wave_crossings[v])


# # The parametrized function to be plotted
# def f(t, amplitude, frequency, offset=0):
#     print(t)
#     return amplitude * np.sin(2 * np.pi * frequency * (t + offset))


# t = np.linspace(0, 1, 1000)

# # Define initial parameters
# init_amplitude = 5
# init_frequency = 3
# init_offset = 0

# # Create the figure and the line that we will manipulate
# fig, ax = plt.subplots()
# (line,) = ax.plot(t, f(t, init_amplitude, init_frequency, init_offset), lw=2)
# ax.set_xlabel("Time [s]")

# # adjust the main plot to make room for the sliders
# fig.subplots_adjust(left=0.25, bottom=0.25)

# # Make a horizontal slider to control the frequency.
# axfreq = fig.add_axes([0.25, 0.12, 0.65, 0.03])
# freq_slider = Slider(
#     ax=axfreq,
#     label="Frequency [Hz]",
#     valmin=0.1,
#     valmax=30,
#     valinit=init_frequency,
# )
# # Make a horizontal slider to control the frequency.
# axoffset = fig.add_axes([0.25, 0.05, 0.65, 0.03])
# offset_slider = Slider(
#     ax=axoffset,
#     label="Offset [t]",
#     valmin=0.0,
#     valmax=30,
#     valinit=init_offset,
# )

# # Make a vertically oriented slider to control the amplitude
# axamp = fig.add_axes([0.1, 0.25, 0.0225, 0.63])
# amp_slider = Slider(
#     ax=axamp,
#     label="Amplitude",
#     valmin=0,
#     valmax=10,
#     valinit=init_amplitude,
#     orientation="vertical",
# )


# # The function to be called anytime a slider's value changes
# def update(val):
#     line.set_ydata(f(t, amp_slider.val, freq_slider.val, offset_slider.val))
#     fig.canvas.draw_idle()


# # register the update function with each slider
# freq_slider.on_changed(update)
# offset_slider.on_changed(update)
# amp_slider.on_changed(update)


# plt.show()
