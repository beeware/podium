#/usr/bin/env python
import io
import re
from setuptools import setup, find_packages


with io.open('./podium/__init__.py', encoding='utf8') as version_file:
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file.read(), re.M)
    if version_match:
        version = version_match.group(1)
    else:
        raise RuntimeError("Unable to find version string.")


with io.open('README.rst', encoding='utf8') as readme:
    long_description = readme.read()


setup(
    name='podium',
    version=version,
    description='A presentation tool for developers.',
    long_description=long_description,
    author='Russell Keith-Magee',
    author_email='russell@keith-magee.com',
    url='http://pybee.org/podium',
    packages=find_packages(exclude=['tests']),
    install_requires=[
    ],
    entry_points={
        'console_scripts': [
            'podium = podium.app.__main__:main',
        ]
    },
    license='New BSD',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: only',
        'Topic :: Software Development',
        'Topic :: Utilities',
    ],
    test_suite='tests',
    options={
        'app': {
            'formal_name': 'Podium',
            'bundle': 'org.pybee',
        },
        'macos': {
            'app_requires': [
                # 'toga[macos]'
            ],
            'icon': 'icons/macos',
        },
    }
)
