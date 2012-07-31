To plot a FITS image in axes::

    import matplotlib.pyplot as plt
    from aplpy2 import WCSAxes

    fig = plt.figure()
    ax = WCSAxes('image.fits')
    ax.grayscale()  # uses pre-loaded data
    fig.savefig('image.png')

Can show the grayscale/colorscale/rgb for a different file as long as dimensions match::

    ax.colorscale('other_image.fits')
    ax.rgb('nice_image.png')

If dimensions don't match::

   ax.grayscale('wrong.fits')
   ...
   DimensionsMismatch: dimensions should be ... but were ...

To overplot a grid in a given system::

    ax.add_grid(system='fk5')

To overlay arbitrary matplotlib patches in pixels::

    from matplotlib.patches import Rectangle
    r = Rectangle((43., 44.), 23., 11.)
    ax.add_patch(r, system='pixel')

To overlay arbitrary matplotlib patches in a given system::

    from matplotlib.patches import Rectangle
    r = Rectangle((272., -44.), 1., 0.8)
    ax.add_patch(r, system='fk5')

And similarly for::

    ax.add_collection(c, system='gal')
    ax.add_line(l, system='fk4')

and so on. Can also provide way to alias::

    ax[fk5].add_patch(...)

to

    ax.add_patch(..., system='fk5')

The former allows::

    ax_fk5 = ax['fk5']

which can then be used without having to repeat ``system=fk5``.

If not specified, ``system`` defaults to the native coordinate system of the original file/WCS header/object.

To add a colorbar::

    ax.add_colorbar()

To add a beam (uses built-in header keywords BMAJ/BMIN/BROT if available)::

    ax.add_beam()

To add a compass::

    ax.add_compass()

which can also take a ``system`` keyword argument.

