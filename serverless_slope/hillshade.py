import numpy as np


def hillshade(normals: np.ndarray, azdeg=315, altdeg=45, fraction=1):
    """Compute raster hillshade from normals

    This is modified from
    https://github.com/openterrain/deploy/blob/ed01ec631b9d8c2757799d237f25b38b77a40b59/openterrain/__init__.py#L291-L354

    This is a slightly modified version of
    matplotlib.colors.LightSource.hillshade, modified to remove the contrast
    stretching (because that uses local min/max values).
    Calculates the illumination intensity for a surface using the defined
    azimuth and elevation for the light source.

    Imagine an artificial sun placed at infinity in some azimuth and
    elevation position illuminating our surface. The parts of the surface
    that slope toward the sun should brighten while those sides facing away
    should become darker.

    Parameters
    ----------
    normals : array-like
        A 2d array (or equivalent) of the height values used to generate an
        illumination map
    azdeg : number, optional
        The azimuth (0-360, degrees clockwise from North) of the light
        source. Defaults to 315 degrees (from the northwest).
    altdeg : number, optional
        The altitude (0-90, degrees up from horizontal) of the light
        source.  Defaults to 45 degrees from horizontal.
    fraction : number, optional
        Increases or decreases the contrast of the hillshade.  Values
        greater than one will cause intermediate values to move closer to
        full illumination or shadow (and clipping any values that move
        beyond 0 or 1). Note that this is not visually or mathematically
        the same as vertical exaggeration.
    Returns
    -------
    intensity : ndarray
        A 2d array of illumination values between 0-1, where 0 is
        completely in shadow and 1 is completely illuminated.
    """
    # Rescale normals to be -1 to 1
    dx = (normals[:, :, 0] / 128) - 1
    dy = (normals[:, :, 1] / 128) - 1

    # Azimuth is in degrees clockwise from North. Convert to radians
    # counterclockwise from East (mathematical notation).
    az = np.radians(90 - azdeg)
    alt = np.radians(altdeg)

    # Calculate the intensity from the illumination angle
    aspect = np.arctan2(dy, dx)
    slope = 0.5 * np.pi - np.arctan(np.hypot(dx, dy))
    intensity = (
        np.sin(alt) * np.sin(slope) +
        np.cos(alt) * np.cos(slope) * np.cos(az - aspect))

    # Apply contrast stretch
    intensity *= fraction

    intensity = np.clip(intensity, 0, 1, intensity)

    return intensity
