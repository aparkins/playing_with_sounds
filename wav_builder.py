import math

def save_wav_file(filename, sample_data, channel_count=1, sample_rate=44100, bytes_per_sample=2):
    data = build_wav_bytes(sample_data, channel_count, sample_rate, bytes_per_sample)
    with open(filename, 'wb') as f:
        f.write(data)

def build_wav_bytes(sample_data, channel_count=1, sample_rate=44100, bytes_per_sample=2):
    if channel_count > 1:
        raise NotImplementedException('multi channel PCM is still a mystery to me. :)')
    assert 0 < bytes_per_sample < 3

    if len(sample_data) % 2 == 1:
        sample_data = sample_data + [0.0]

    max_sample = 2 ** (bytes_per_sample * 8 - 1) - 1
    min_sample = -max_sample - 1
    sample_range = max_sample - min_sample

    def _round(x):
        r, q = math.modf(x)
        q = math.floor(q)
        if math.isclose(r, 0.5) or r > 0.5:
            return q+1
        return q

    mapped_samples = []
    for sample in sample_data:
        normalized = (sample + 1.0) / 2.0
        scaled = _round(normalized * sample_range)
        adjusted = scaled + min_sample
        capped = max(min_sample, min(adjusted, max_sample))
        mapped_samples.append(capped)

    header_bytes = _wav_header(
        len(mapped_samples) * bytes_per_sample,
        channel_count,
        sample_rate,
        bytes_per_sample,
    )
    data_bytes = _map_to_bytes(mapped_samples, bytes_per_sample, True)

    return header_bytes + data_bytes


def _wav_header(data_length, channel_count=1, sample_rate=44100, bytes_per_sample=2):
    FMT_CHUNK_SIZE = 16

    sub_data_size = (
        4 + # WAVE
        8 + # fmt chunk header
        FMT_CHUNK_SIZE +
        8 + # data chunk header
        data_length
    )
    block_align = channel_count * bytes_per_sample
    byte_rate = sample_rate * channel_count * bytes_per_sample
    audio_format = 1 # PCM

    assert data_length > 0
    assert data_length % 2 == 0
    assert sub_data_size < (2 ** (8 * 4))
    assert 0 < channel_count < 2 ** (8 * 2)
    assert 0 < sample_rate < 2 ** (8 * 4)
    assert 0 < bytes_per_sample < 3
    assert 0 < block_align < 2 ** (8 * 2)

    header = [
        'RIFF',
        sub_data_size,
        'WAVE',

        'fmt ',
        FMT_CHUNK_SIZE,
        audio_format | (channel_count << 16),
        sample_rate,
        byte_rate,
        block_align | ((bytes_per_sample * 8) << 16),

        'data',
        data_length,
    ]

    return _map_to_bytes(header)


def _map_to_bytes(data, word_size=4, signed_ints=False):
    byte_data = b''
    for word in data:
        if isinstance(word, str):
            byte_data += word.encode()
        elif isinstance(word, int):
            byte_data += word.to_bytes(length=word_size, byteorder='little', signed=signed_ints)
        else:
            raise TypeError("Invalid word in data: {}".format(word))
    return byte_data



def _preview_bytes(byte_array):
    for b in byte_array:
        print('%02x' % b)

