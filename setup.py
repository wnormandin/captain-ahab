from setuptools import setup, find_packages

__version__ = '0.0.1'


install_requires = (
    'pywin32',
    'numpy',
    'opencv-python',
    'pillow',
    'click',
    'click-log',
    'python-dotenv'
)

setup(
    name='nw-captain-ahab',
    author_email='bill@pokeybill.us',
    author='pokeybill',
    packages=find_packages(),
    license='MIT',
    description='Captain Ahab handles your fishing needs',
    install_requires=install_requires,
    entry_points={'console_scripts': ['captain-ahab=captain_ahab.cli:cli']}
)
