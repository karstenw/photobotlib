from setuptools import setup

setup(name='photobot',
      version='1.2',
      packages=['photobot'],
      install_requires=[
            # silenced due to security warning for pillow <8.3.2; should still run with python2
            # 'Pillow == 6.2.2; python_version < "3.0.0"',
            # 'Pillow >= 7.1.0; python_version >= "3.5.0"']
            'Pillow >= 8.3.2; python_version >= "3.5.0"']
      )

