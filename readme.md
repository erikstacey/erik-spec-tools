# erik-spec-tools

Written by Erik Stacey during the Summer of 2020 to aid in analyzing spectra of suspected magnetic B-type stars.
Requires a working installation of IDL and J. H. Grunhut's spectroscopic analysis tools (which are not publicly
available to my knowledge). This program is utilized by running process_single_dir.py or process_blended_binary.py
from a command line in the working directory, where the spectrum of interest is stored. See doc string of process_single_dir.py for more details.

As this program was quickly thrown together for a summer research project when I was very early in my career,
it is poorly structured and documented. Nonetheless, this program removed a significant degree of manual input necessary
to use the underlying IDL code in its original form, and managed to reduce spectrum analysis time by approximately 50%. I still occasionally use this program when I have to analyze the odd spectrum.

I've added this program to my github as a part of my portfolio and to establish the canon version of this program in case
I need to use it in the future. 