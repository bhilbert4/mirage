#! /usr/bin /env python

"""Download reference files, create library, and set environment variable
"""
import tarfile


NIRCAM_URLS = []
NIRISS_URLS = []
FGS_URLS = []

NIRCAM_GRIDDED_PSF_URLS = []
NIRCAM_INDIVIDUAL_PSF_URLS = []
NIRISS_GRIDDED_PSF_URLS = []
NIRISS_INDIVIDUAL_PSF_URLS = []
FGS_GRIDDED_PSF_URLS = []
FGS_INDIVIDUAL_PSF_URLS = []


def download_reffiles(directory, instrument='all', psf_version='gridded'):
    """Download tarred and gzipped reference files

    Parameters
    ----------
    directory : str
        Directory into which the reference files are placed. This will
        be the directory set to the MIRAGE_DATA environment variable

    instrument : str
        If ``all``: download all files. If the name of an individual
        instrument, download only the data for that instrument

    psf_version : str
        If ``gridded``: download new PSf library
        If ``something else``: download old PSF library
    """
    file_list = get_file_list(instrument, psf_version)

    for filename in file_list:
        requests.download(filename, directory)
        local_file = os.path.join(directory, filename)

        # Unzip and untar file
        file_object = tarfile.open(name=local_file, mode='r:gz', )
        file_object.extractall(path=directory)


def get_file_list(instruments, library_version):
    """Collect filenames"""
    urls = []
    instrument_names = [name.strip().lower() for name in instruments.split(',')]

    if 'all' in instrument_names:
            urls = NIRCAM_URLS + NIRISS_URLS + FGS_URLS
            if library_version == 'gridded':
                urls.extend(NIRCAM_GRIDDED_PSF_URLS)
                urls.extend(NIRISS_GRIDDED_PSF_URLS)
                urls.extend(FGS_GRIDDED_PSF_URLS)
            else:
                urls.extend(NIRCAM_INDIVIDUAL_PSF_URLS)
                urls.extend(NIRISS_INDIVIDUAL_PSF_URLS)
                urls.extend(FGS_INDIVIDUAL_PSF_URLS)
    else:
        for instrument_name in instrument_names:
            if instrument_name.lower() == 'nircam':
                urls.extend(NIRCAM_URLS)
                if library_version == 'gridded':
                    urls.extend(NIRCAM_GRIDDED_PSF_URLS)
                else:
                    urls.extend(NIRCAM_INDIVIDUAL_PSF_URLS)
            elif instrument_name.lower() == 'niriss':
                urls.extend(NIRISS_URLS)
                if library_version == 'gridded':
                    urls.extend(NIRISS_GRIDDED_PSF_URLS)
                else:
                    urls.extend(NIRISS_INDIVIDUAL_PSF_URLS)
            elif instrument_name.lower() == 'fgs':
                urls.extend(FGS_URLS)
                if library_version == 'gridded':
                    urls.extend(FGS_GRIDDED_PSF_URLS)
                else:
                    urls.extend(FGS_INDIVIDUAL_PSF_URLS)
    return urls
