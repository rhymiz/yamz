#!/usr/bin/env python3
from setuptools import setup


setup(name='environments',
      version='0.0.1',
      description='A super hacky way to manage environment specific configuration',
      author='Lemuel Boyce',
      author_email='lemuelboyce@gmail.com',
      packages=['environments'],
      url='https://github.com/rhymiz/environments',
      include_package_data=True,
      zip_safe=False,
      license='MIT',
      python_requires='>=3.6',
      install_requires=[
        'PyYAML==3.13'
      ])
