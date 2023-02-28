import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from icecream import ic
from os.path import dirname, join as pjoin
from scipy.io import wavfile
import scipy.io


data_dir = pjoin(dirname(scipy.io.__file__), "tests", "data")
wave_filename = pjoin(data_dir, "test-44100Hz-2ch-32bit-float-be.wav")
wave_filename = "pulse-mod.wav"
wave_samplerate, data = wavfile.read(wave_filename)
wave_num_channels = data.shape[1]
wave_duration = data.shape[0] / wave_samplerate
ic(wave_filename, wave_samplerate, wave_num_channels, wave_duration)

wave_samples = np.arange(0, data.shape[0])
wave_time = wave_samples / wave_samplerate
wave_data = data[:, 0]
wave_data = wave_data / np.max(np.abs(wave_data))
last = 0
wave_crossings = []
for i, v in enumerate(wave_data):
    if np.sign(v) == 0:
        continue
    if np.sign(v) != last:
        wave_crossings.append(i)
    last = np.sign(v)

windows_cache = {}
ic(wave_crossings[:10])


def find_windows(freq_approx=440, start_crossing=0):
    freq_approx = int(freq_approx)
    start_crossing = int(start_crossing)
    name = f"{freq_approx}-{start_crossing}"
    if name in windows_cache:
        return windows_cache[name]
    num_crossings = len(wave_crossings)
    samples_approx = wave_samplerate / freq_approx
    windows = []
    # ic("find_windows", freq_approx, start_crossing, num_crossings)
    i = start_crossing
    last_i = -1
    while i < num_crossings:
        closest = [i, 100000]
        crossing1 = wave_crossings[i]
        for j in range(i, min(num_crossings, i + 30)):
            crossing2 = wave_crossings[j]
            dif = np.abs((crossing2 - crossing1) - samples_approx)
            if dif < closest[1]:
                closest = [j, dif]
        windows.append([i, closest[0]])
        i = closest[0]
        if last_i == i:
            break
        last_i = i
    windows_cache[name] = windows
    return windows


def f(freq_approx=440, start_crossing=0, crossing_index=0, amplitude=1):
    windows = find_windows(freq_approx, start_crossing)
    window = windows[int(np.floor(len(windows) * (crossing_index - 0.01)))]
    samples = [wave_crossings[window[0]], wave_crossings[window[1]]]
    x = np.arange(samples[0], samples[1])
    y = wave_data[samples[0] : samples[1]]
    return x, y * amplitude


# Define initial parameters
init_amplitude = 1
init_frequency = 261
init_offset = 0

for i in range(10):
    find_windows(init_frequency, i)

# Create the figure and the line that we will manipulate
fig, ax = plt.subplots()
x, y = f(init_frequency, 0, 0, 1)
(line,) = ax.plot(x, y, lw=2)
ax.set_xlabel("Time [s]")
ax.set_autoscale_on(False)
# adjust the main plot to make room for the sliders
fig.subplots_adjust(left=0.25, bottom=0.25)

# Make a horizontal slider to control the frequency.
axfreq = fig.add_axes([0.25, 0.12, 0.65, 0.03])
freq_slider = Slider(
    ax=axfreq,
    label="Freq. Guess [Hz]",
    valmin=20,
    valmax=800,
    valstep=1,
    valinit=init_frequency,
)

axoffset = fig.add_axes([0.25, 0.08, 0.65, 0.03])
offset_slider = Slider(
    ax=axoffset,
    label="Zero-crossing offset",
    valmin=0,
    valmax=10,
    valinit=0,
    valstep=1,
)

axindex = fig.add_axes([0.25, 0.04, 0.65, 0.03])
index_slider = Slider(
    ax=axindex,
    label="Position [s]",
    valmin=0,
    valmax=wave_duration,
    valinit=0,
)

# Make a vertically oriented slider to control the amplitude
axamp = fig.add_axes([0.1, 0.25, 0.0225, 0.63])
amp_slider = Slider(
    ax=axamp,
    label="Amplitude",
    valmin=0,
    valmax=10,
    valinit=init_amplitude,
    orientation="vertical",
)


# The function to be called anytime a slider's value changes
def update(val):
    x, y = f(
        freq_slider.val,
        offset_slider.val,
        index_slider.val / wave_duration,
        amp_slider.val,
    )
    line.set_ydata(y)
    line.set_xdata(x / wave_samplerate)
    ax.fill_between(x, y, 0, color="blue", alpha=0.1)
    est_freq = wave_samplerate / (x[-1] - x[0])
    line.set_label(f"freq ~ {est_freq:.1f} Hz")
    ax.legend(handles=[line])
    ax.set_xlim(min(x) / wave_samplerate, max(x) / wave_samplerate)
    ax.set_ylim(-1, 1)
    ax.axhline(y=0.0, color="k", linestyle="--")
    fig.canvas.draw()
    fig.canvas.flush_events()


# register the update function with each slider
freq_slider.on_changed(update)
offset_slider.on_changed(update)
index_slider.on_changed(update)
amp_slider.on_changed(update)

update(None)
plt.suptitle(wave_filename)
plt.show()
