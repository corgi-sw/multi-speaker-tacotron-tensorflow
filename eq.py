import os
import numpy as np
import librosa as lr
from pysndfx.dsp import AudioEffectsChain

def effect0():
    effect = (AudioEffectsChain().vol(6, 'dB', '0.02'))

    return effect

def effect1():
    effect = \
    (AudioEffectsChain()
     .equalizer(50, 1.0, -10.0)
     .equalizer(100, 1.0, -10.0)
     .equalizer(200, 1.0, -10.0)
     .equalizer(500, 1.0, -10.0)
     .equalizer(1000, 1.0, -10.0)
     .equalizer(2000, 1.0, -10.0)
     .equalizer(5000, 1.0, -10.0)
     .equalizer(10000, 1.0, -10.0)
     .equalizer(20000, 1.0, -10.0))

    return effect

def effect2():
    effect = \
    (AudioEffectsChain()
     .equalizer(50, 1.0, 10.0)
     .equalizer(100, 1.0, 10.0)
     .equalizer(200, 1.0, 10.0)
     .equalizer(500, 1.0, 10.0)
     .equalizer(1000, 1.0, 10.0)
     .equalizer(2000, 1.0, 10.0)
     .equalizer(5000, 1.0, 10.0)
     .equalizer(10000, 1.0, 10.0)
     .equalizer(20000, 1.0, 10.0))

    return effect

def effect3():
    effect = \
    (AudioEffectsChain()
     .highshelf()
     .reverb()
     .phaser()
     .delay()
     .lowshelf())

    return effect

def set_effect(e, filename):

    ext = ".wav"
    mono, sr = lr.load(filename + ext, sr=None)

    effect = ''
    if e == 0:
        effect = effect0()
    elif e == 1:
        effect = effect1()
    elif e == 2:
        effect = effect2()
    elif e == 3:
        effect = effect3()

    y = effect(mono)
    print(filename + "_" + str(e) + ext)
    lr.output.write_wav(filename + "_" + str(e) + ext, y, sr)
    assert lr.util.valid_audio(y, mono=False)

apply_audio_effects1 = \
    (AudioEffectsChain()
     .equalizer(50, 1.0, -10.0)
     .equalizer(100, 1.0, -10.0)
     .equalizer(200, 1.0, -10.0)
     .equalizer(500, 1.0, -10.0)
     .equalizer(1000, 1.0, -10.0)
     .equalizer(2000, 1.0, -10.0)
     .equalizer(5000, 1.0, -10.0)
     .equalizer(10000, 1.0, -10.0)
     .equalizer(20000, 1.0, -10.0))

apply_audio_effects2 = \
    (AudioEffectsChain()
     .equalizer(50, 1.0, 10.0)
     .equalizer(100, 1.0, 10.0)
     .equalizer(200, 1.0, 10.0)
     .equalizer(500, 1.0, 10.0)
     .equalizer(1000, 1.0, 10.0)
     .equalizer(2000, 1.0, 10.0)
     .equalizer(5000, 1.0, 10.0)
     .equalizer(10000, 1.0, 10.0)
     .equalizer(20000, 1.0, 10.0))

static_folder = os.getcwd() + "/static_folder/"
infile =  static_folder + 'Raw.0000.wav'
mono, sr = lr.load(infile, sr=None)
stereo, _ = lr.load(infile, sr=None, mono=False)
outfile = 'test_output.wav'

def main():

    y = apply_audio_effects1(stereo)
    lr.output.write_wav('1.wav', y, sr)
    assert lr.util.valid_audio(y, mono=False)

    y = apply_audio_effects2(stereo)
    lr.output.write_wav('2.wav', y, sr)
    assert lr.util.valid_audio(y, mono=False)

    y = apply_audio_effects1(stereo)
    lr.output.write_wav('3.wav', y, sr)
    assert lr.util.valid_audio(y, mono=False)

    y = apply_audio_effects2(stereo)
    lr.output.write_wav('4.wav', y, sr)
    assert lr.util.valid_audio(y, mono=False)

def test_file_to_file():
    apply_audio_effects(infile, outfile)
    y = lr.load(outfile, sr=None, mono=False)[0]
    lr.output.write_wav('test_file_to_file.wav', y, sr)
    assert lr.util.valid_audio(y, mono=False)

def test_ndarray_to_ndarray():
    y = apply_audio_effects(mono)
    lr.output.write_wav('test_ndarray_to_ndarray_mono.wav', y, sr)
    assert lr.util.valid_audio(y)

    y = apply_audio_effects(stereo)
    lr.output.write_wav('test_ndarray_to_ndarray_stereo.wav', y, sr)
    assert lr.util.valid_audio(y, mono=False)

def test_ndarray_to_file():
    apply_audio_effects(mono, outfile)
    y = lr.load(outfile, sr=None)[0]
    lr.output.write_wav('test_ndarray_to_file_mono.wav', y, sr)
    assert lr.util.valid_audio(y)

    apply_audio_effects(stereo, outfile)
    y = lr.load(outfile, sr=None, mono=False)[0]
    lr.output.write_wav('test_ndarray_to_file_stereo.wav', y, sr)
    assert lr.util.valid_audio(y, mono=False)

def test_file_to_ndarray():
    y = apply_audio_effects(infile)
    lr.output.write_wav('test_file_to_ndarray.wav', y, sr)
    assert lr.util.valid_audio(y, mono=False)

if __name__ == "__main__":
	main()