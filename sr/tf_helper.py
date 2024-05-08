import numpy as np
import tensorflow as tf
import librosa


# Set the seed value for experiment reproducibility.
seed = 42
tf.random.set_seed(seed)
np.random.seed(seed)


def get_melspectrogram(waveform):
    input_len = 16000
    waveform = waveform[:input_len]
    zero_padding = tf.zeros(
        [16000] - tf.shape(waveform),
        dtype=tf.float32)
    # Cast the waveform tensors' dtype to float32.
    waveform = tf.cast(waveform, dtype=tf.float32)
    equal_length = tf.concat([waveform, zero_padding], 0)
    # Calcula o espectrograma linear
    spectrogram = tf.signal.stft(equal_length, frame_length=255, frame_step=128)
    spectrogram = tf.abs(spectrogram)

    # Converte o espectrograma linear para o espectrograma de mel
    num_spectrogram_bins = spectrogram.shape[-1]
    num_mel_bins = 40
    mel_weights = tf.signal.linear_to_mel_weight_matrix(
        num_mel_bins, num_spectrogram_bins, 16000, 20, 4000)
    mel_spectrogram = tf.matmul(tf.square(spectrogram), mel_weights)
    mel_spectrogram = tf.math.log(mel_spectrogram + 1e-6)  # Logaritmo para melhorar a escala

    return mel_spectrogram[..., tf.newaxis]  # Adiciona um novo eixo para manter a mesma estrutura


from scipy.signal import resample

def preprocess_audiobuffer(waveform):
    # Calcula o número de amostras após a reamostragem
    num_samples = int(len(waveform) * 16000 / 44100)

    # Reamostrar o waveform
    waveform = resample(waveform, num_samples)

    # Normaliza de [-32768, 32767] para [-1, 1]
    waveform = waveform / 32768

    waveform = tf.convert_to_tensor(waveform, dtype=tf.float32)
    spectogram = get_melspectrogram(waveform)
    spectogram = tf.expand_dims(spectogram, 0)

    return spectogram