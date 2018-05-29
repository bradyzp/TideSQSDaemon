# -*- coding: utf-8 -*-

from setuptools import setup

requirements = [
    'tidegravity',
    'boto3',
    'flask',
    'marshmallow'
]

setup(
    name='TideServer',
    version='0.2alpha-1',
    packages=['src'],
    install_requires=requirements,
    python_requires='>=3.5.*',
    description="General purpose server application to supply tide corrections via HTTP REST API or AWS SQS",
    author="Zachery Brady",
    author_email="bradyzp@dynamicgravitysystems.com",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux'
    ]
)
