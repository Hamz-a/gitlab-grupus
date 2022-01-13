import setuptools
from distutils.core import setup

with open('requirements.txt') as f:
    requirements = f.readlines()

setup(
    name='gitlab-grupus',
    description='Clone gitlab repositories by group ID',
    version='0.0.1',
    packages=['gitlab_grupus'],
    install_requires=requirements,
    zip_safe=True,
    license='MIT',
    keywords='gitlab grupus git clone',
    entry_points={
        'console_scripts': [
            'ggrupus = gitlab_grupus.main:main'
        ]
    },
)