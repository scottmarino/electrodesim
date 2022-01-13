#!/usr/bin/env python3
# Graphing program to solve Laplace's equations

import numpy as np
import matplotlib.pyplot as plt
import sys

def load_boundary(darray, gridsize):
	clx = int(0.5*gridsize*(1.0-PWID))
	cux = gridsize - clx

	capth = (2.0*PTH + GAP)*gridsize

	cly1 = int(0.5*(gridsize-capth))
	cuy1 = int(cly1 + gridsize*PTH)
	
	cly2 = int(cly1 + gridsize*(GAP + PTH))
	cuy2 = gridsize - cly1

	darray[clx:cux, cly1:cuy1] = -VOLTAGE
	darray[clx:cux, cly2:cuy2] = VOLTAGE

	gridlim = gridsize - 1
	darray[:,0:1] = 0
	darray[:,gridlim:gridsize] = 0
	darray[0:1,:] = 0
	darray[gridlim:gridsize,:] = 0
	return darray

inputstr = """
Please enter the number of iterations, grid size, plate thickness, width, 
spacing, and voltage in a comma separated list as such:

	ITERATIONS, GRIDSIZE, THICKNESS, WIDTH, SPACING, VOLTAGE

Noninteger values for iteration number and gridsize will be rounded. 
The thickness, width, and spacing must be given as fractions/decimal ratios 
of gridsize.
"""

while True:
	instr = input(inputstr)
	try:
		instrlist = instr.split(',')
		nlist = [float(x.strip()) for x in instrlist]
		GRIDSIZE = int(nlist[1])
		ITER = int(nlist[0])
		PTH = nlist[2]
		PWID = nlist[3]
		GAP = nlist[4]
		VOLTAGE = nlist[5]
	except ValueError:
		print("\nInvalid input, try again\n", file=sys.stderr)
	except IndexError:
		print("\nNot enough values, try again.\n", file=sys.stderr)
	else:
		break

PTH = nlist[2]
PWID = nlist[3]
GAP = nlist[4]
VOLTAGE = nlist[5]

VDAT = np.zeros(GRIDSIZE**2).reshape(GRIDSIZE,GRIDSIZE)
load_boundary(VDAT, GRIDSIZE)

# From the relaxation method, the value at any point will be the average of the
# points around it, so we can add the surrounding 4 points thru rolling and 
# divide by 4.

for i in range(256):
	VDAT += np.roll(VDAT,-1,axis=0) # Roll up
	VDAT += np.roll(VDAT,1,axis=0) # Down
	VDAT += np.roll(VDAT,-1,axis=1) # Left
	VDAT += np.roll(VDAT,1,axis=1) # Right
	VDAT /= 4

	load_boundary(VDAT, GRIDSIZE) # Reset boundaries

# Transpose coordinates for graphing
plotarr = np.flipud(VDAT.transpose())

f1, ax1 = plt.subplots()
ax1.set_title('Electrode Voltage Simulator')
picture = ax1.imshow(plotarr, interpolation='none',cmap='jet')
f1.show()

#f1.savefig('p1_graph3.eps',format='eps') # For saving plots

input("\nPress <Enter> to exit...\n")

