#! /usr/bin/env python

"""This module contains code for reading and writing source spectra into
hdf5 files. This format is needed as input to the disperser package
used to create dispersed seed images

Authors
-------

    - Bryan Hilbert

Use
---

    This script is intended to be executed as such:

    ::

        from mirage.catalogs import hdf5_catalog
        spectra_dict = hdf5_catalog.open('my_catalog_file.hdf5')

        hdf5_catalog.save(spectra_dict, 'my_updated_catalog_file.hdf5')
"""

import astropy.units as u
import h5py


def open(filename):
    """Read in contents of an hdf5 file

    Parameters
    ----------
    filename : str
        Name of file to be opened

    Returns
    -------
    contents : dict
        Dictionary containing the contents of the file
        Dictionary format:
        keys are the index numbers of the sources corresponding to the segmentation map
        Each value is a dictionary containing keys 'wavelengths' and 'fluxes'.
        'wavelengths' is a tuple of (list of wavelength values, wavelength units string)
        'fluxes' is a tuple of (list of flux values, flux units string)
    """
    contents = {}
    with h5py.File(filename, 'r') as file_obj:
        for key in file_obj.keys():
            dataset = file_obj[key]
            waves = dataset[0]
            fluxes = dataset[1]
            wave_units = dataset.attrs['wavelength_units']
            flux_units = dataset.attrs['flux_units']

            # Convert the unit strings into astropy.units Unit object
            wave_units = string_to_units(wave_units)
            flux_units = string_to_units(flux_units)

            contents[int(key)] = {'wavelengths': (waves, wave_units)
                                  'fluxes': (fluxes, flux_units)}
    return contents


def save(contents, filename):
    """Save a dictionary into an hdf5 file

    Paramters
    ---------
    contents : dict
        Dictionary of data. Dictionary format:
        keys are the index numbers of the sources corresponding to the segmentation map
        Each value is a dictionary containing keys 'wavelengths' and 'fluxes'.
        'wavelengths' is a tuple of (list of wavelength values, wavelength units string)
        'fluxes' is a tuple of (list of flux values, flux units string)

    filename : str
        Name of hdf5 file to produce
    """
    with h5py.File(filename, "w") as file_obj:
        for key in contents.keys():
            flux, flux_units = contents[key]['fluxes']
            wavelength, wavelength_units = contents[key]['wavelengths']

            # If units are astropy.units Units objects, change to strings
            if isinstance(wavelength_units, u.core.PrefixUnit):
                wavelength_units = units_to_string(wavelength_units)
            if isinstance(flux_units, u.core.PrefixUnit):
                flux_units = units_to_string(flux_units)

            if not isinstance(wavelength_units, str):
                raise ValueError("Wavelength units must be a string.")
            if not isinstance(flux_units, str):
                raise ValueError("Flux units must be a string.")

            dset = file_obj.create_dataset(str(key), data=[wavelength, flux], dtype='f', compression="gzip",
                                           compression_opts=9)

            # Set dataset units. Not currently inspected by mirage.
            dset.attrs[u'wavelength_units'] = wavelength_units
            dset.attrs[u'flux_units'] = flux_units


def string_to_units(unit_string):
    """Convert a string containing units to an astropy.units Quantity

    Parameters
    ----------
    unit_string : str
        String containing units (e.g. 'erg/sec/cm/cm/A/A')

    Returns
    -------
    units : astropy.units Quantity
    """
    try:
        return u.Unit(unit_string)
    except ValueError as e:
        print(e)


def units_to_string(quantity):
    """Convert the units of an astropy.units Quantity to a string

    Parameters
    ----------
    quantity : astropy.units Quantity

    Returns
    -------
    unit_string : str
        String representation of the units in quantity
    """
    return quantity.unit.to_string()
