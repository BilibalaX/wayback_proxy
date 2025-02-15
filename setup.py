from os import path
import re
from setuptools import setup, find_packages
import sys
import versioneer


# NOTE: This file must remain Python 2 compatible for the foreseeable future,
# to ensure that we error out properly for people with outdated setuptools
# and/or pip.
min_version = (3, 6)
if sys.version_info < min_version:
    error = """
wayback does not support Python {0}.{1}.
Python {2}.{3} and above is required. Check your Python version like so:

python3 --version

This may be due to an out-of-date pip. Make sure you have pip >= 9.0.1.
Upgrade pip like so:

pip install --upgrade pip
""".format(*(sys.version_info[:2] + min_version))
    sys.exit(error)

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as readme_file:
    readme = readme_file.read()

# Delimits a setup.py-compatible requirement name/version from the extras that
# only pip supports (environment info, CLI options, etc.).
# https://pip.pypa.io/en/stable/reference/pip_install/#requirements-file-format
REQUIREMENT_DELIMITER = re.compile(r';|--')


def read_requirements(filename):
    """
    Read a pip requirements file into a list of standard package requirements.
    """
    with open(path.join(here, filename)) as file:
        return [REQUIREMENT_DELIMITER.split(line, 1)[0]
                for line in file.read().splitlines()
                if (not line.startswith('git+https://') and
                    not line.startswith('#') and
                    not line.startswith('-r'))]


setup(
    name='wayback',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description="Python API to Internet Archive Wayback Machine",
    long_description=readme,
    author="Environmental Data Governance Initiative",
    author_email='EnviroDGI@protonmail.com',
    url='https://github.com/edgi-govdata-archiving/wayback',
    python_requires='>={}'.format('.'.join(str(n) for n in min_version)),
    packages=find_packages(exclude=['docs', 'tests']),
    entry_points={
        'console_scripts': [
            # 'command = some.module:some_function',
        ],
    },
    include_package_data=True,
    package_data={
        'wayback': [
            # When adding files here, remember to update MANIFEST.in as well,
            # or else they will not be included in the distribution on PyPI!
            # 'path/to/data_file',
        ]
    },
    install_requires=read_requirements('requirements.txt'),
    extras_require={
        'dev': read_requirements('requirements-dev.txt'),
        'docs': read_requirements('requirements-docs.txt'),
        'test': read_requirements('requirements-test.txt'),
    },
    license="BSD (3-clause)",
    project_urls={
        'Documentation': 'https://wayback.readthedocs.io/en/stable/',
        'Changelog': 'https://wayback.readthedocs.io/en/stable/release-history.html',
        'Source code': 'https://github.com/edgi-govdata-archiving/wayback',
        'Issues': 'https://github.com/edgi-govdata-archiving/wayback/issues',
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
    ],
)
