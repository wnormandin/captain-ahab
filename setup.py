from setuptools import setup, find_packages

__version__ = '0.0.1'


install_requires = (
    'pywin32',
    'numpy',
    'opencv-python',
    'pillow',
    'click'
)

setup(
    name='nw-captain-ahab',
    author_email='normandindev@gmail.com',
    author='Bill Normandin',
    packages=find_packages(),
    license='MIT',
    description='Captain Ahab handles your fishing needs',
    install_requires=install_requires
)
