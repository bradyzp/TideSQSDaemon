# -*- coding: utf-8 -*-

from setuptools import setup

requirements = [
    'tidegravity',
    'boto3'
]

setup(
    name='TideSQSDaemon',
    version='0.1alpha-1',
    packages=['TideSQSDaemon'],
    install_requires=requirements,
    python_requires='>=3.5.*',
    description="AWS SQS Daemon to consume/produce tide gravity corrections.",
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
