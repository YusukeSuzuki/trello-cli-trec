from setuptools import setup, find_packages


setup(
  name='trello-cli-trec',
  version='0.0.1',
  packages=find_packages(
    ),
  entry_points={
    'console_scripts': [
      'trec = trec.main:main',
      ]
    },
  install_requires=[
    'requests',
    'appdirs',
    ],
  )
