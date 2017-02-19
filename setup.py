from setuptools import setup, find_packages

import blue_daisy


with open('README.rst') as readme:
    README = readme.read()


setup(
    name='blue-daisy',
    version=blue_daisy.__version__,
    url='https://github.com/bawabu/blue-daisy',
    license='MIT License',
    author='Evans Murithi',
    author_email='murithievans80@gmail.com',
    packages=find_packages(exclude=['tests', 'docs']),
    description=(
        'A daemon using bluetooth to enable an android application to '
        'control your computer.'
    ),
    long_description=README,
    include_package_data=True,
    install_requires=[
        'PyBluez==0.22',
        'python-daemon==2.1.2',
        'PyUserInput==0.1.11'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: No Input/Output (Daemon)',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3'
    ]
)
