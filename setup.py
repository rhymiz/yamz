#!/usr/bin/env python3
from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='yamz',
      version='0.2.0',
      description='An easy way to manage environment specific configuration',
      long_description=long_description,
      long_description_content_type='text/markdown',
      author='Lemuel Boyce',
      author_email='lemuelboyce@gmail.com',
      packages=find_packages(exclude=['tests']),
      url='https://github.com/rhymiz/yamz',
      include_package_data=True,
      zip_safe=False,
      license='MIT',
      python_requires='>=3.6',
      install_requires=[
          'PyYAML>=5.1'
      ],
      classifiers=[
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.6",
          "Programming Language :: Python :: 3.7",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
      ])
