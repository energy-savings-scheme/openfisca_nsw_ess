# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name="openfisca_nsw_safeguard",
    version="0.0.1",
    author="Department of Planning Industry and Environment - NSW Government",
    author_email = 'liam.mccann@environment.nsw.gov.au',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Topic :: Scientific/Engineering :: Information Analysis",
        ],
    description="An OpenFisca extension for the NSW Energy Security Safeguard ",
    keywords = 'Energy Savings Safeguard',
    license="http://www.fsf.org/licensing/licenses/agpl-3.0.html",
    url = "https://github.com/energy-savings-scheme/openfisca_nsw_safeguard",
    include_package_data = True,  # Will read MANIFEST.in
    data_files = [],
    install_requires = [
        'OpenFisca-Core[web-api] @ git+https://github.com/energy-savings-scheme/openfisca-core.git',
        'openfisca_nsw_base @ git+https://github.com/Openfisca-NSW/openfisca_nsw_base.git'
    ],
    extras_require = {
        "dev": [
            "autopep8 ==1.4.4",
            "flake8 >=3.5.0,<3.8.0",
            "flake8-print",
            "pycodestyle >=2.3.0,<2.6.0",  # To avoid incompatibiopenfisclity with flake
            ]
        },
    packages=find_packages(),
    )
