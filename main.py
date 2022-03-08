import audiofilter as af
from matplotlib import pyplot as plt

audio, sample_rate = af.validate_load_audio(af.examples('me'))

plt.subplot(2, 2, 1)
af.wave_plot(audio, sample_rate)
plt.subplot(2, 2, 2)

af.freq_plot(audio, sample_rate)

audio, sample_rate = af.add_background_noise(audio, sample_rate, background_noise='gaussian')

plt.subplot(2, 2, 3)
af.wave_plot(audio, sample_rate)
plt.subplot(2, 2, 4)
af.freq_plot(audio, sample_rate)

plt.show()

af.play_sound(audio, sample_rate)
