#!/usr/bin/env python3
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='yamz',
      version='0.0.4',
      description='An easy way to manage environment specific configuration',
      long_description=long_description,
      author='Lemuel Boyce',
      author_email='lemuelboyce@gmail.com',
      packages=['yamz'],
      url='https://github.com/rhymiz/yamz',
      include_package_data=True,
      zip_safe=False,
      license='MIT',
      python_requires='>=3.6',
      install_requires=[
          'PyYAML==3.13'
      ],
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
      ])
