#!/usr/bin/env python
import io
import re
from setuptools import setup, find_packages


with io.open('./src/podium/__init__.py', encoding='utf8') as version_file:
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
    url='https://beeware.org/project/projects/applications/podium',
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    data_files=[
        ('resources', [
            'resources/notes-template.html',
            'resources/print-template.html',
            'resources/slide-template.html',
            'resources/remark.js',
            'resources/animate.css',
        ]),
        ('resources/themes/default', [
            'resources/themes/default/style.css',
            'resources/themes/default/DroidSerif.woff',
            'resources/themes/default/UbuntuMono-Regular.woff',
            'resources/themes/default/YanoneKaffeesatz-Regular.woff',
        ])
    ],
    include_package_data=True,
    install_requires=[
    ],
    license='New BSD',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development',
        'Topic :: Utilities',
    ],
    test_suite='tests',
    zip_safe=False,
    options={
        'app': {
            'formal_name': 'Podium',
            'bundle': 'org.beeware',
            'document_types': {
                'deck': {
                    'description': 'Podium Slide Deck',
                    'extension': 'podium',
                    'icon': 'icons/podium-deck',
                    'url': 'https://beeware.org/project/projects/applications/podium/',
                }
            }
        },
        'macos': {
            'app_requires': [
                'toga-cocoa>=0.3.0.dev11'
            ],
            'icon': 'icons/podium',
        },
        'linux': {
            'app_requires': [
                'toga-gtk>=0.3.0.dev11'
            ],
        }
    }
)
