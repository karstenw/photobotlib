from setuptools import setup

setup(name='photobot',
      version='1.2',
      packages=['photobot'],
      install_requires=[
            'Pillow == 6.2.2; python_version < "3.0.0"',
            'Pillow; python_version >= "3.0.0"']
      )

