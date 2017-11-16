import math


DEFAULT_SAMPLE_RATE = 44100


def gen_triangle_wave(frequency, amplitude, duration=1.0, sample_rate=DEFAULT_SAMPLE_RATE):
    period = 1.0 / frequency
    per_region = period / 4
    slope = amplitude / per_region
    sample_size = 1.0 / sample_rate

    samples = []
    current_sample_x = 0.0
    while current_sample_x < duration:
        normalized = math.fmod(current_sample_x, period)

        if normalized < per_region:
            samples.append(slope * normalized)
        elif normalized < (per_region * 3):
            samples.append((-slope * normalized) + (amplitude * 2))
        else:
            samples.append((slope * normalized) - (amplitude * 4))

        current_sample_x += sample_size

    return samples


def gen_sine_wave(frequency, amplitude, duration=1.0, sample_rate=DEFAULT_SAMPLE_RATE):
    sample_size = 1.0 / sample_rate

    samples = []
    current_sample_x = 0.0
    while current_sample_x < duration:
        sample = amplitude * math.sin(2.0 * math.pi * frequency * current_sample_x)
        samples.append(sample)
        current_sample_x += sample_size

    return samples


def gen_fluctuating_sine_wave(starting_freq, ending_freq, pulse_freq, amplitude, duration=1.0, sample_rate=DEFAULT_SAMPLE_RATE):
    sample_size = 1.0 / sample_rate
    pulse_amplitude = abs(starting_freq - ending_freq) / 2.0

    samples = []
    current_sample_x = 0.0
    while current_sample_x < duration:
        main_beat = 2.0 * math.pi * pulse_amplitude * current_sample_x
        modifier = pulse_amplitude * math.sin(2.0 * math.pi * current_sample_x * pulse_freq)
        sample = amplitude * math.sin(main_beat + modifier)
        samples.append(sample)
        current_sample_x += sample_size

    return samples


def transpose_samples(first_samples, second_samples):
    if len(first_samples) > len(second_samples):
        tmp = first_samples
        first_samples = second_samples
        second_samples = tmp

    first_samples += [ 0.0 ] * (len(second_samples) - len(first_samples))

    result_samples = []
    for i in range(len(first_samples)):
        sample_a = first_samples[i]
        sample_b = second_samples[i]
        result_sample = max(-1.0, min(1.0, sample_a + sample_b))
        result_samples.append(result_sample)

    return result_samples

