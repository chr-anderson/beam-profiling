# beam-profiling
Short python script to enable easy profiling of laser beams using a CCD.

This script estimates a laser beam's 1/e^2 radius by fitting intensity profile data to a Gaussian curve. The script uses curve_fit from scipy.optimize, which fits a user-defined function via least-squares regression. The fit is plotted so its suitability can be verified.

Best results are obtained by imaging a beam head-on with a CCD, then gathering grayscale profile data using ImageJ along only the width of the beam (not the full image width). Curve fitting works best if the detector is not fully saturated at non-central points, so a neutral density filter might be necessary to reduce brightness on the CCD.

**Optional console arguments.**
Extra arguments that can be passed to the interpreter are:
1. csv file name or file path
2. Cutoff for ignoring saturated values during curve fitting. See below formore information. Of course, it's best to just not saturate the CCD.

**Setting the max_cutoff value.**
The max_cutoff value allows the user to list a saturation value as an additional argument from the console (255 for grayscale). If any data are at or above this value, they'll be removed before fitting a Gaussian curve. This lets the user avoid artificially flattening the fit just because the CCD sensitivity maxed out before getting to the center of the spot.

A max_cutoff value of 255 will be used if none is specified.

**Parameter guesses to start least squares.**
The script fits provided data to a curve of the form:

I = I<sub>0</sub>exp(-2(x-x<sub>0</sub>)<sup>2</sup> / r<sub>0</sub><sup>2</sup>).

The initial guesses for least squares are:
* I<sub>0</sub> = full saturation value
* x<sub>0</sub> = middle of the range of data x values
* r<sub>0</sub> = 35% of the range of data x values
