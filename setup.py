# -*- encoding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function

import io
from glob import glob
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import splitext

from setuptools import find_packages
from setuptools import setup


def read(*names, **kwargs):
    with io.open(
            join(dirname(__file__), *names),
            encoding=kwargs.get('encoding', 'utf8')
    ) as fh:
        return fh.read()


setup(
    name='opera-phantom',
    version='0.0.1.preview',
    license='GPL-3.0',
    description='TBD.',
    long_description='TBD.',
    author='Francesco Calcagnini',
    author_email='francesco@calcagnini.it',
    url='https://github.com/DoremyR3d/opera-phantom',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        # 'Development Status :: 5 - Production/Stable',
        # 'Intended Audience :: Developers',
        # 'License :: OSI Approved :: BSD License',
        # 'Operating System :: Unix',
        # 'Operating System :: POSIX',
        # 'Operating System :: Microsoft :: Windows',
        # 'Programming Language :: Python',
        # 'Programming Language :: Python :: 2.7',
        # 'Programming Language :: Python :: 3',
        # 'Programming Language :: Python :: 3.4',
        # 'Programming Language :: Python :: 3.5',
        # 'Programming Language :: Python :: 3.6',
        # 'Programming Language :: Python :: 3.7',
        # 'Programming Language :: Python :: Implementation :: CPython',
        # 'Programming Language :: Python :: Implementation :: PyPy',
        # uncomment if you test on these interpreters:
        # 'Programming Language :: Python :: Implementation :: IronPython',
        # 'Programming Language :: Python :: Implementation :: Jython',
        # 'Programming Language :: Python :: Implementation :: Stackless',
        # 'Topic :: Utilities',
    ],
    project_urls={
        # 'Changelog': 'https://github.com/ionelmc/python-nameless/blob/master/CHANGELOG.rst',
        'Issue Tracker': 'https://github.com/DoremyR3d/opera-phantom/issues',
    },
    keywords=[
        # eg: 'keyword1', 'keyword2', 'keyword3',
    ],
    python_requires='>=3.7',
    install_requires=[
        'attrs'
        # eg: 'aspectlib==1.1.1', 'six>=1.7',
    ],
    tests_require=[
        'pytest',
        'attrs'
    ],
    extras_require={
        # eg:
        #   'rst': ['docutils>=0.11'],
        #   ':python_version=="2.6"': ['argparse'],
    },
    setup_requires=[
        'pytest-runner'
    ],
    entry_points={
        # 'console_scripts': [
        #     'nameless = nameless.cli:main',
        # ]
    },
)
