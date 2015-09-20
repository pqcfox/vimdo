from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'DESCRIPTION.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='vimdo',
      version='1.0.0',
      description='Vim-like todo list',
      long_description=long_description,
      url='https://github.com/useanalias/vimdo',
      author='Alias User',
      author_email='use.an.alias@gmail.com',
      license='MIT',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.2',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
      ],
      keywords='vim todo productivity',
      packages=find_packages(),
      install_requires=['curses'],
      entry_points={
          'console_scripts': [
              'vimdo=vimdo.vimdo:main'
          ]
      }
      )
