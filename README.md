# RSM (Really Small Music)

A very, VERY lossy music compressor I made overnight that retains musical notes.

## How does it work?

RSM takes in an audio file, performs an FFT for every tenth of a second, and extracts the values of 88 frequencies (A0 through C8, as on a standard piano), quantizes the values to fit in one byte each, and writes the values to a file. Given this file, it can convert the compressed values to sine wave notes and write the audio to a wav file to listen to. When uncompressing to a wav file, melodies are mostly discernible, despite the extremely small size of the compressed file.

Every 88 bytes is a new frame, spanning 1/10 of a second. The 88 values are the volumes of the 88 keys in ascending order. The file format itself is headerless, defaulting to 32-bit floats, 2 channels, and 44100 Hz when unzipped.

The compressed format can be shrunk further using a standard file compressor (zip/xz/gzip/7z), for a total of up to about 1/80 the size of its mp3 equivalent (given that the mp3 uses 32-bit floats, 2 channels, and 44100 Hz).

## Why use this?

The main reason why I wanted something like this was to be able to train a generative music AI without the overhead of buying hardware or paying for cloud hardware. The output quality isn't great, but it's useful for newcomers to AI if they want a quick model that's easier and cheaper to train. This method is easier than similar methods (such as training AI on MIDI files or ABC notation) because most training music on the internet can be scraped as a standard audio file, but not as MIDI (due to not shipping with MIDI). The audio quality of MIDI is obviously much better than RSM when coupled with a soundfont or VST player though, and this is the tradeoff.

## Dependencies

Older versions may or may not work. Tested on Debian Bookworm.

* numpy >= 1.24.2

## Usage

To convert from standard audio to RSM:

`python3 rsm.py zip /path/to/audio.wav /path/to/audio.rsm`

To uncompress RSM to standard audio:

`python3 rsm.py unzip /path/to/audio.rsm /path/to/audio.wav`
