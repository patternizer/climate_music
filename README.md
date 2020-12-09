# climate_music

Python workflow for translating climatic anomaly timeseries into musical frequencies mapped onto a 108 key piano roll in LMMS. The MIDI file is generated using [midiutil](https://github.com/duggan/midiutil) by Mark Conway Wirt. Output video hue and cropping applied using OBS.

* climate data reader
* algorithm to map data onto music frequencies
* automated extraction of note list
* automated conversion to MIDI output
* MP4 recording of LMMS Piano Roll output

## Contents

* `climate-music.py` - python reader and algorithm

The first step is to clone the latest climate_music code and step into the check out directory: 

    $ git clone https://github.com/patternizer/climate_music.git
    $ cd climate_music

### Using Standard Python

The code should run with the [standard CPython](https://www.python.org/downloads/) installation and was tested 
in a conda virtual environment running a 64-bit version of Python 3.8.3.

climate_music scripts can be run from sources directly, once the dependencies are resolved. You will need to download the CRUTEM4 dataset: https://crudata.uea.ac.uk/cru/data/temperature/CRUTEM4-gl.dat. To import the generated MIDI file into the Piano Roll (https://lmms.io/wiki/index.php?title=Piano_Roll_Editor) you will need also the Linux LMMS music editing suite installed on your system downloadable from: https://lmms.io/.

Run with:

    $ python climate-music.py

## License

climate_music.py is distributed under terms and conditions of the [Open Government License](http://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/).

## Contact information

* [Michael Taylor](michael.a.taylor@uea.ac.uk)

