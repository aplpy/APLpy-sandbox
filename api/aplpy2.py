# About
# -----
#
# The APLpy module for plotting Astronomical images was originally designed
# when the Matplotlib API was still in flux, and as such, we implemented many
# of our own methods to simplify things for users. For example, we added many
# methods to customize the look of e.g. axis and tick labels. However, this
# ends up confusing users, because the API is different for a matplotlib or
# APLpy plot, and it would be better to make the API become more consistent
# with Matplotlib so that users only need to learn once how to do this. This
# document presents a proposed new API that makes APLpy objects behave much
# more like Matplotlib plots, and makes it easier to combine the two.
#
# Note that FITSFigure is not defined in the new API, so we can easily leave
# the old class and methods for backward compatibility initially.
#
# Initialization
# --------------
#
# To plot a FITS image in axes:

import aplpy
import matplotlib.pyplot as plt

fig = plt.figure()
ax = aplpy.WCSAxes('image.fits')
fig.add_axes(ax)
ax.grayscale()  # uses pre-loaded data
fig.savefig('image.png')

# We could also consider having a custom Figure class that adds
# ``add_wcs_axes`` - this gives us the option of overriding 'savefig' to
# auto-set the DPI resolution for example.

fig = aplpy.figure()
ax = fig.add_wcs_axes('image.fits')
ax.grayscale()
fig.savefig('image.png')

# By default, the axes would be added with the equivalent of subplot(1,1,1) but this can be customized with subplot and axes arguments:

ax = aplpy.WCSAxes('image.fits', subplot=(2, 2, 1))
ax = aplpy.WCSAxes('image.fits', axes=[0.1, 0.1, 0.8, 0.8])
ax = fig.add_wcs_axes('image.fits', subplot=(3, 3, 2))
ax = fig.add_wcs_axes('image.fits', axes=[0.1, 0.1, 0.4, 0.4])

# Images
# ------
#
# By default, ax.colorscale, ax.grayscale, and ax.rgb would show the image
# that was used to initialize the axes. We can also show the
# grayscale/colorscale/rgb for a different file as long as dimensions match:

ax.colorscale('other_image.fits')
ax.rgb('nice_image.png')

# and if dimensions don't match, an error is raised:

ax.grayscale('wrong.fits')
# raises DimensionsMismatch - dimensions should be ... but were ...

# Data cubes
# ----------
#
# Similarly to the current APLpy API, multi-dimensional cubes are supported.
# When initializing the WCSAxes, ``slices=`` and ``dimensions=`` arguments
# should be specified. For example, to take the 10th slice in the third
# dimension:

ax = aplpy.WCSAxes('cube.fits', slices=[9])

# To choose the first and third dimension and pick the 5th slice in the second dimension:

ax = aplpy.WCSAxes('cube.fits', dimensions=[0,2], slices=[4])

# and so on...

# We may also want to make it so that we only choose the slices when we
# actually plot, so that we can easily plot the slices of a cube without
# re-loading the cube every time:

for i in range(10):
    ax.grayscale(slices=[i])

# Finally, we should consider the possibility of specifying the actual value
# rather than the index for the slices, if this is possible.

# Coordinate grids
# ----------------

# To overplot a grid in a given system:

ax.add_grid(system='fk5')

# Multiple coordinate grids can be overplotted:

ax.add_grid(system='fk5')
ax.add_grid(system='galactic')

# Axis labels
# -----------
#
# The system for the axis labels can be changed from the default (which is
# the system from the file):

ax.set_labels_system('galactic')

# and we may want to consider the possibility of having multiple label
# systems (e.g. one of left and bottom, and one on top and right)
#
# Patches/shapes/lines
# --------------------
#
# To overlay arbitrary matplotlib patches in pixels:

from matplotlib.patches import Rectangle
r = Rectangle((43., 44.), 23., 11.)
ax.add_patch(r, system='pixel')

# To overlay arbitrary matplotlib patches in a given system:

from matplotlib.patches import Rectangle
r = Rectangle((272., -44.), 1., 0.8)
ax.add_patch(r, system='fk5')

# And similarly:

ax.add_collection(c, system='gal')
ax.add_line(l, system='fk4')

# We can consider adding an alias:

ax['fk5'].add_patch(...)

# which is equivalent to:

ax.add_patch(..., system='fk5')

# The former allows:

ax_fk5 = ax['fk5']

# which can then be used without having to repeat system=fk5.
#
# If not specified, 'system' defaults to the native coordinate system of the
# original file/WCS header/object.
#
# Common overlays
# ---------------
#
# To add a colorbar:

ax.add_colorbar()

# To add a beam (uses built-in header keywords BMAJ/BMIN if available):

ax.add_beam()

# And if the header keywords are not availbale:

ax.add_beam(major=0.2, minor=0.04, angle=45.)

# To add a compass:

ax.add_compass()

# which can also take a 'system' keyword argument.