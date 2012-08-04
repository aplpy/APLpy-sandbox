# Initialization
# --------------

# Given the significant changes in API, we could initially develop this as
# 'aplpy2' and then eventually create a compatibility layer for the original
# APLpy interface and then rename to 'aplpy'

# To plot a FITS image in axes:

import aplpy2
import matplotlib.pyplot as plt

fig = plt.figure()
ax = aplpy2.WCSAxes('image.fits')
fig.add_axes(ax)
ax.grayscale()  # uses pre-loaded data
fig.savefig('image.png')

# We could also consider having a custom Figure class that adds
# ``add_wcs_axes`` - this gives us the option of
# overriding 'savefig'.

fig = aplpy2.figure()
ax = fig.add_wcs_axes('image.fits')
ax.grayscale()
fig.savefig('image.png')

# By default, the axes would be added with the equivalent of subplot(1,1,1) but this can be customized with subplot and axes arguments:

ax = aplpy2.WCSAxes('image.fits', subplot=(2, 2, 1))
ax = aplpy2.WCSAxes('image.fits', axes=[0.1, 0.1, 0.8, 0.8])
ax = fig.add_wcs_axes('image.fits', subplot=(3, 3, 2))
ax = fig.add_wcs_axes('image.fits', axes=[0.1, 0.1, 0.4, 0.4])

# Images
# ------

# By default, ax.colorscale, ax.grayscale, and ax.rgb would show the image
# that was used to initialize the axes. We can also show the
# grayscale/colorscale/rgb for a different file as long as dimensions match:

ax.colorscale('other_image.fits')
ax.rgb('nice_image.png')

# If dimensions don't match:

ax.grayscale('wrong.fits')
# raises DimensionsMismatch - dimensions should be ... but were ...

# Coordinate grids
# ----------------

# To overplot a grid in a given system:

ax.add_grid(system='fk5')

# Patches/shapes/lines
# --------------------

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

ax[fk5].add_patch(...)

# which is equivalent to:

ax.add_patch(..., system='fk5')

# The former allows:

ax_fk5 = ax['fk5']

# which can then be used without having to repeat system=fk5.

# If not specified, 'system' defaults to the native coordinate system of the original file/WCS header/object.

# Common overlays
# ---------------

# To add a colorbar:

ax.add_colorbar()

# To add a beam (uses built-in header keywords BMAJ/BMIN if available):

ax.add_beam()

# And if the header keywords are not availbale:

ax.add_beam(major=0.2, minor=0.04, angle=45.)

# To add a compass:

ax.add_compass()

# which can also take a 'system' keyword argument.

