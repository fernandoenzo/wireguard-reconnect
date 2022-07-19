#!/usr/bin/env python3
# encoding:utf-8

# More on how to configure this file here: https://setuptools.readthedocs.io/en/latest/setuptools.html#metadata
from autopackage.parsers.setup_parser import SetupParser
from setuptools import find_packages

name = 'wireguard-reconnect'

version = '1.0.6'

description = 'This program performs unattended handling of selected WireGuard interfaces, bringing them up and down depending on whether there is connectivity to the server or not, ' \
              'or simply bringing them up and keeping them up.\nWorks great combined with systemd.'

with open("README.md", "r") as fh:
    long_description = fh.read()

author = 'Fernando Enzo Guarini'
author_email = 'fernandoenzo@gmail.com'

url = 'https://github.com/fernandoenzo/wireguard-reconnect'
download_url = 'https://github.com/fernandoenzo/wireguard-reconnect/releases'

packages = find_packages()

licencia = 'AGPLv3+'

zip_safe = True

keywords = 'wireguard net vpn ip link ping route routing'

python_requires = '>=3.7'

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Environment :: Console',
    'Intended Audience :: End Users/Desktop',
    'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
    'Natural Language :: English',
    'Operating System :: POSIX :: Linux',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Topic :: Communications',
    'Topic :: Internet',
    'Topic :: System :: Networking',
    'Topic :: Utilities',
]

entry_points = {
    'console_scripts': [
        'wireguard-reconnect = wireguard_reconnect.wireguard_reconnect:main',
    ]
}

SetupParser(name=name, version=version, packages=packages, description=description, long_description=long_description, long_description_content_type="text/markdown", author=author,
            author_email=author_email, url=url, download_url=download_url, license=licencia, python_requires=python_requires, keywords=keywords, classifiers=classifiers, entry_points=entry_points,
            zip_safe=zip_safe)
