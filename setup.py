# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
from setuptools import setup


try:
    long_description = open(b'README.rst', 'rt').read()
except IOError:
    long_description = ""

try:
    long_description += open(b'ChangeLog.rst', 'rt').read().strip()
except IOError:
    pass


MODULE_PATH = os.path.join(os.getcwd(), "encrypted_id", "__init__.py")


def find_this(search, filename=MODULE_PATH):
    """Take a string and a filename path string and return the found value."""
    if not search:
        return
    for line in open(str(filename)).readlines():
        if search.lower() in line.lower():
            line = line.split("=")[1].strip()
            if "'" in line or '"' in line or '"""' in line:
                line = line.replace("'", "").replace('"', '').replace('"""', '')
            return line


print(find_this("__version__"))

setup(
    name="django-encrypted-id",
    description="Encrypted IDs for Django Models",
    long_description=long_description,

    version=find_this("__version__"),

    author=find_this("__author__"),
    author_email=find_this("__email__"),
    maintainer=find_this("__author__"),
    maintainer_email=find_this("__email__"),

    url=find_this("__source__"),
    license=find_this("__license__"),


    install_requires=[
        "Django>=1.8", "PyCrypto",
    ],


    packages=["encrypted_id"],
    zip_safe=True,


    keywords=['Django', 'Web'],


    classifiers=[

        'Development Status :: 5 - Production/Stable',

        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Other Audience',

        'Natural Language :: English',

        'Operating System :: OS Independent',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS :: MacOS X',

        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',

        'Programming Language :: Python :: Implementation :: CPython',

        'Topic :: Software Development',

    ],
)
