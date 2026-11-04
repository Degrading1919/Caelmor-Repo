"""Broad diffuse pigments for authored timber and stone construction roles."""
import numpy as np

from .surface_conditions import smooth
from .surface_patterns import _noise


def timber_pigment(u, v, stock, arris, craft):
    """Tint longitudinal ribbons and narrow hewn facets on structural wood."""
    # U follows the member's long edge on its side charts. The ribbon width is
    # large enough to read from the approach, with broken ends along the grain.
    warp = .023 * _noise(u, v, 1.4, 4.5, 673)
    ribbons = .74 * _noise(u, v+warp, 1.6, 12., 677)
    ribbons += .26 * _noise(u, v, 3.9, 7., 683)
    prepared = smooth(-.28, .68, ribbons+.18*stock)
    dark = smooth(.11, .68, -ribbons)
    work = {'ROUGH': .74, 'STANDARD': 1., 'FINE': 1.10}[craft]
    honey = work*(.14+.56*prepared+.19*arris*(.40+.60*prepared))
    return 1. + honey[:, None]*np.array([.69, .59, .34]) - dark[:, None]*np.array([.10,.105,.075])


def masonry_pigment(position, normal, stock):
    """Brush-sized mineral tones and restrained accents on real upper bevels."""
    x,y,z = position.T
    nx,ny,nz = normal.T
    face = (np.maximum(np.abs(nx),np.abs(ny))>.98)
    upper_bevel = (nz>.26)&(nz<.62)&(np.maximum(np.abs(nx),np.abs(ny))>.76)
    # Use actual height and horizontal run so the pigment has the same
    # direction on opposite faces. Independent from the stock color field.
    beds = .78*_noise(x+y,z,2.0,8.4,697) + .22*_noise(x-y,z,4.0,4.0,701)
    deposit = smooth(-.24,.62,beds+.15*stock)
    darker = smooth(.08,.68,-beds)
    accent = upper_bevel*(.09+.11*deposit)
    return (1. + (face*deposit)[:,None]*np.array([.19,.17,.115])
            - (face*darker)[:,None]*np.array([.078,.061,.036])
            + accent[:,None]*np.array([1.,.96,.82]))
