#!/usr/bin/env python3

# Really Small Music (RSM)

import numpy
import math
import sys
import wave

def allNotes(sr):
    a4 = 440 * (sr / 44100)

    for i in range(88):
        yield (a4 / 16) * (2 ** (i / 12))

def main():
    if len(sys.argv) < 4:
        return

    if sys.argv[1] == 'zip':
        print('Loading...')

        with wave.open(sys.argv[2], 'rb') as f:
            nchannels = f.getnchannels()
            sr = f.getframerate()
            audio = numpy.frombuffer(f.readframes(f.getnframes()), dtype=numpy.int16).astype(numpy.float32)

        audio = audio.reshape(-1, nchannels).T.reshape(nchannels, -1)

        tmpAudio = audio[0]

        for i in range(1, len(audio)):
            tmpAudio += audio[i]

        tmpAudio *= 1 / max(tmpAudio)
        audio = tmpAudio

        print('Compressing...')

        song = []

        for i in range(0, len(audio) - int(sr / 10), int(sr / 20)):
            print(f'Progress: {int(i / (sr / 10))} / {(len(audio) - int(sr / 10)) // int(sr / 10)}')

            transform = abs(numpy.fft.fft(audio[i : i + int(sr / 10)]))

            notes = []

            for note in allNotes(sr):
                notes.append(int((transform[int(note / 10)] / int(sr / 20)) * 256))

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
        allNotes2 = [item for item in allNotes(44100)]

        signals = {}
        peak = (2 ** 15) - 1

        for note in allNotes(44100):
            signals[note] = numpy.array([math.sin((t * 2 * math.pi * note) / 44100) for t in range(4410)])

        with wave.open(sys.argv[3], "wb") as f:
            f.setnchannels(1)
            f.setsampwidth(2)
            f.setframerate(44100)
            
            for notes in song:
                print(f'Progress: {index + 1} / {len(song)}')
    
                chunk = numpy.zeros(2205)
    
                for i in range(len(allNotes2)):
                    width = 44100 / allNotes2[i]
                    start = int((index * 2205) % width)
                    chunk += signals[float(allNotes2[i])][start : start + 2205] * (notes[i] / 2205)

                biggest = max(numpy.abs(chunk))
                
                if biggest > peak:
                    peak *= peak / biggest

                if biggest != 0:
                    chunk *= peak / biggest
                    
                f.writeframes(chunk.astype(numpy.int16).tobytes())
    
                index += 1

if __name__ == '__main__':
    main()
