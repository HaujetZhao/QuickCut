from array import array
import audioop
import math

FORMAT = {1: "b", 2: "h", 4: "i"}
_EPSILON = 1e-10


def to_array(data, sample_width, channels):
    fmt = FORMAT[sample_width]
    if channels == 1:
        return array(fmt, data)
    return separate_channels(data, fmt, channels)


def extract_single_channel(data, fmt, channels, selected):
    samples = array(fmt, data)
    return samples[selected::channels]


def average_channels(data, fmt, channels):
    all_channels = array(fmt, data)
    mono_channels = [
        array(fmt, all_channels[ch::channels]) for ch in range(channels)
    ]
    avg_arr = array(
        fmt,
        (round(sum(samples) / channels) for samples in zip(*mono_channels)),
    )
    return avg_arr


def average_channels_stereo(data, sample_width):
    fmt = FORMAT[sample_width]
    arr = array(fmt, audioop.tomono(data, sample_width, 0.5, 0.5))
    return arr


def separate_channels(data, fmt, channels):
    all_channels = array(fmt, data)
    mono_channels = [
        array(fmt, all_channels[ch::channels]) for ch in range(channels)
    ]
    return mono_channels


def calculate_energy_single_channel(x, sample_width):
    energy_sqrt = max(audioop.rms(x, sample_width), _EPSILON)
    return 20 * math.log10(energy_sqrt)


def calculate_energy_multichannel(x, sample_width, aggregation_fn=max):
    energies = (calculate_energy_single_channel(xi, sample_width) for xi in x)
    return aggregation_fn(energies)
