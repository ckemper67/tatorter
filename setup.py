# tatorter
# Copyright (C) 2018  Daniel Llin Ferrero
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''
Created on 27.11.2017

:author: DLF
'''

from setuptools import setup
from setuptools import find_packages


setup(
    name='tatorter',
    version='0.1',
    description='A simple script to rename Tatort episode video files to a unique pattern.',
    author='DLFW',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    install_requires=['fuzzywuzzy','python-Levenshtein','mechanicalsoup','pathlib'],
    license='GPL 3',
    scripts=['scripts/tatorter','scripts/tatorter.py'],
    classifiers=[
        'Development Status :: early but stable',
        'Environment :: Console',
        'License :: GPL 3',
    ],
)
