# Exploring transformations in matplotlib - based on pywcsgrid2 code

import numpy as np
from matplotlib.transforms import Transform
from matplotlib.path import Path


class CurvedTransform(Transform):
    def __init__(self):
        """
        Create a new WCS transform.
        """
        Transform.__init__(self)

    def transform_path(self, path):
        return Path(self.transform(path.vertices), path.codes)

    transform_path.__doc__ = Transform.transform_path.__doc__

    transform_path_non_affine = transform_path
    transform_path_non_affine.__doc__ = Transform.transform_path_non_affine.__doc__


class WcsWorld2PixelTransform(CurvedTransform):
    """
    """
    input_dims = 2
    output_dims = 2
    is_separable = False

    def __init__(self, wcs):
        CurvedTransform.__init__(self)
        self.wcs = wcs

    def transform(self, world):

        xw, yw = world[:, 0], world[:, 1]

        xp, yp = self.wcs.wcs_world2pix(xw, yw, 1)
        xp, yp = xp - 1, yp - 1
        pixel = np.concatenate((xp[:, np.newaxis], yp[:, np.newaxis]), 1)

        return pixel

    transform.__doc__ = Transform.transform.__doc__

    transform_non_affine = transform
    transform_non_affine.__doc__ = Transform.transform_non_affine.__doc__

    def inverted(self):
        return WcsPixel2WorldTransform(self.wcs)

    inverted.__doc__ = Transform.inverted.__doc__


class WcsPixel2WorldTransform(CurvedTransform):
    """
    """
    input_dims = 2
    output_dims = 2
    is_separable = False

    def __init__(self, wcs):
        CurvedTransform.__init__(self)
        self.wcs = wcs

    def transform(self, pixel):

        xp, yp = pixel[:, 0], pixel[:, 1]

        xp, yp = xp + 1, yp + 1
        xw, yw = self.wcs.wcs_pix2world(xp, yp, 1)
        world = np.concatenate((xw[:, np.newaxis], yw[:, np.newaxis]), 1)

        return world

    transform.__doc__ = Transform.transform.__doc__

    transform_non_affine = transform
    transform_non_affine.__doc__ = Transform.transform_non_affine.__doc__

    def inverted(self):
        return WcsWorld2PixelTransform(self.wcs)

    inverted.__doc__ = Transform.inverted.__doc__

if __name__ == "__main__":

    from astropy.wcs import WCS

    wcs = WCS('1904-66_AZP.fits.gz')
    trans = WcsWorld2PixelTransform(wcs)

    from matplotlib.patches import Rectangle
    from matplotlib.lines import Line2D
    import matplotlib.pyplot as plt

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    ax.set_xlim(-3000., 3000.)
    ax.set_ylim(-3000., 3000.)

    for lon in np.linspace(0., 360., 19):
        xw = np.repeat(lon, 100)
        yw = np.linspace(-90., 90., 100)
        l = Line2D(xw, yw, transform=trans + ax.transData)
        ax.add_line(l)

    for lat in np.linspace(-90., 90., 19):
        xw = np.linspace(-180., 180., 100)
        yw = np.repeat(lat, 100)
        l = Line2D(xw, yw, transform=trans + ax.transData)
        ax.add_line(l)

    fig.savefig('1904-66_AZP.png')
