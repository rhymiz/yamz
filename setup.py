#!/usr/bin/env python3
from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='yamz',
      version='0.3.0a1',
      description='An easy way to manage environment specific configuration',
      long_description=long_description,
      long_description_content_type='text/markdown',
      author='Lemuel Boyce',
      author_email='lemuelboyce@gmail.com',
      packages=find_packages(exclude=['tests']),
      url='https://github.com/rhymiz/yamz',
      include_package_data=True,
      zip_safe=True,
      license='MIT',
      scripts=['bin/yamz'],
      python_requires='>=3.6',
      install_requires=[],
      classifiers=[
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.6",
          "Programming Language :: Python :: 3.7",
          "Programming Language :: Python :: 3.8",
          "Programming Language :: Python :: 3.9",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
      ])
