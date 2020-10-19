'''
This script estimates a laser beam's 1/e^2 radius by fitting intensity profile
data to a Gaussian curve. The script uses curve_fit from scipy.optimize, which
fits a user-defined function via least-squares regression. The fit is plotted
so its suitability can be verified.

Best results are obtained by imaging a beam head-on with a CCD, then
gathering grayscale profile data using ImageJ along only the width of the beam
(not the full image width). Curve fitting works best if the detector is not
fully saturated at non-central points, so a neutral density filter might be
necessary to reduce brightness on the CCD.

Optional console arguments:
    1. csv file name or file path
    2. Cutoff for ignoring saturated values during curve fitting. See below for
       more information. Of course, it's best to just not saturate the CCD.
'''

import numpy as np
import csv
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import sys

try:
    file = sys.argv[1] # specify your csv as 1st console arg or change below
except:
    file = 'ex_profile.csv' # Change csv or specify file path here

'''
The max_cutoff value allows the user to list a saturation value as an
additional argument from the console (255 for grayscale). If any data are at or
above this value, they'll be removed before fitting a Gaussian curve. This lets
the user avoid artificially flattening the fit just because the CCD sensitivity
maxed out before getting to the center of the spot.

A max_cutoff value of 255 will be used if none is specified.
'''
try:
    max_cutoff = float(sys.argv[2])
except:
    max_cutoff = 255 # Change this to the desired cutoff or specify at console

background = 0 # Enter your background value here
x, y = [], [] # Lists for 1-D pixel positions and corresponding intensities
# Reads csv, skipping rows with headers or non-numeric entries
with open(file) as file:
    csvreader = csv.reader(file, delimiter = ',')
    for index, row in enumerate(csvreader):
        try:
            float(row[0])
            float(row[1])
        except:
            print('Skipping invalid data in row ' + str(index))
            skip = True
        if not skip:
            x.append(float(row[0]))
            y.append(float(row[1]) - background)
        skip = False

# Removing data values above max_cutoff
del_idx = [] # List of indices to remove
for index, yval in enumerate(y):
    if yval >= max_cutoff - background:
        del_idx.append(index)
x = [x for i, x in enumerate(x) if i not in del_idx] # removing items at...
y = [y for i, y in enumerate(y) if i not in del_idx]# flagged indices
print('Removed ' + str(len(del_idx)) + ' saturated values')

# Defining the function to fit
def Gauss(x, I0, x0, r0):
    return(I0 * np.exp( (-2 * (x - x0)**2) / r0**2 ))

'''
Parameter guesses to start least squares. The guesses are:
    * I0 = full saturation value
    * x0 = middle of the range of data x values
    * r0 = 35% of the range of data x values
'''
p0 = [max_cutoff, 0.5 * (x[-1] - x[0]), 0.35 * (x[-1] - x[0])]

#Least squares fit
popt, _ = curve_fit(Gauss, x, y, p0 = p0)
print('Estimated beam radius is %.2f' % (popt[2]))

plt.figure(figsize = (8, 6))
plt.plot(x, y, 'k.', label='Data')
plt.plot(np.arange(max(x), step = 0.01), Gauss(np.arange(max(x), step = 0.01), *popt), 'b-', label='Fit')
plt.legend(fontsize = 14)
plt.xticks(fontsize = 14)
plt.yticks(fontsize = 14)
diam_width = np.arange(popt[1] - popt[2], popt[1] + popt[2], step = 0.01)
# Regions that would fall within the beam radius are shaded light blue:
plt.fill_between(diam_width, Gauss(diam_width, *popt), alpha = 0.3)
plt.figtext(0.5, 0.025, r'$\frac{1}{e^2}$ beam radius = %.2f' % (popt[2]),
    ha = 'center', fontsize = 14)
plt.title('Center Profile Data and Gaussian Fit',
    fontsize = 20,
    weight = 'bold')
plt.show()
