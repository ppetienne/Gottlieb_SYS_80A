from setuptools import setup

setup(name='Devil_Dare_MotherBoard',
      version='1.0.0',
      packages=['Pinball.Devil_Dare'],
      entry_points={
          'console_scripts': [
              'my_project = my_project.__main__:main'
          ]
      },
      )