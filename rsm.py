#!/usr/bin/env python3

# Really Small Music (RSM)

import numpy
import numpy.fft
import torch
import torchaudio
import math
import sys

def allNotes():
    for i in range(88):
        yield (440 / 16) * (2 ** (i / 12))

def main():
    if len(sys.argv) < 4:
        return

    if sys.argv[1] == 'zip':
        print('Loading...')
        audio, sr = torchaudio.load(sys.argv[2])
        audio = torchaudio.functional.resample(audio, sr, 44100)

        tmpAudio = audio[0]

        for i in range(1, len(audio)):
            tmpAudio += audio[i]

        audio = tmpAudio / len(audio)
        audio = audio.numpy()

        print('Compressing...')

        song = []

        for i in range(0, len(audio) - 4410, 4410):
            print(f'Progress: {(i // 4410)} / {(len(audio) - 4410) // 4410}')

            transform = abs(numpy.fft.fft(audio[i : i + 4410]))

            notes = []

            for note in allNotes():
                notes.append(int((transform[int(note / 10)] / 2205) * 256))

            song.append(notes)

        print('Exporting...')

        with open(sys.argv[3], 'wb') as f:
            for chunk in song:
                f.write(bytes(bytearray(chunk)))

    elif sys.argv[1] == 'unzip':
        print('Importing...')

        song = []

        with open(sys.argv[2], 'rb') as f:
            while len(chunk := f.read(88)) > 0:
                chunk = numpy.array(list(bytearray(chunk)), dtype=numpy.float32)
                chunk /= 256
                chunk *= 2205
                song.append(chunk)

        index = 0
        orig = numpy.array([])
        allNotes2 = [item for item in allNotes()]

        signals = {}

        for note in allNotes():
            signals[note] = numpy.array([math.sin((t * 2 * math.pi * note) / 44100) for t in range(4410)])

        for notes in song:
            print(f'Progress: {index + 1} / {len(song)}')

            chunk = numpy.zeros(4410)

            for i in range(len(allNotes2)):
                chunk += signals[float(allNotes2[i])] * (notes[i] / 2205)

            orig = numpy.append(orig, chunk)

            if index % 1000 == 999:
                torchaudio.save(sys.argv[3], torch.FloatTensor(numpy.array([orig, orig])), 44100)

            index += 1

        print('Saving...')
        torchaudio.save(sys.argv[3], torch.FloatTensor(numpy.array([orig, orig])), 44100)

if __name__ == '__main__':
    main()
