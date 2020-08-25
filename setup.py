from setuptools import setup 

setup(
  name='manageservice',
  version='0.1',
  description='A python service that can be used to pull a master branch from GitHub and start it',
  author='seanorourke',
  author_email='sean.f.orourke@gmail.com.com',
  license='MIT',
  packages=['manageservice'],
  entry_points = {
    'console_scripts': ['manageservice=manageservice.command_line:main'],
    },
  install_requires=[
    "pygithub",
    "configparser",	
    ],
  zip_safe=False,
)
