#!/usr/bin/env python3
"""The setup script."""

from setuptools import find_packages, setup

with open('README.md') as f:
    readme = f.read()

# Runtime requirements.
inst_reqs = ["lambda-proxy>=5.1.1", "imageio", "numpy", "boto3"]
setup_requirements = ['setuptools >= 38.6.0', 'twine >= 1.11.0']

# yapf: disable
setup(
    author="Kyle Barron",
    author_email='kylebarron2@gmail.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Serverless, worldwide slope angle shading tiles",
    install_requires=inst_reqs,
    license="MIT license",
    long_description=readme,
    long_description_content_type='text/markdown',
    name='serverless-slope',
    packages=find_packages(include=['serverless_slope', 'serverless_slope.*']),
    setup_requires=setup_requirements,
    url='https://github.com/kylebarron/serverless-slope',
    version='0.1.0',
    zip_safe=False
)
