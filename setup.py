import io
import os
import re

from setuptools import find_packages
from setuptools import setup


def read(filename):
    filename = os.path.join(os.path.dirname(__file__), filename)
    text_type = type(u"")
    with io.open(filename, mode="r", encoding='utf-8') as fd:
        return re.sub(text_type(r':[a-z]+:`~?(.*?)`'), text_type(r'``\1``'), fd.read())


setup(
    name="aws-lambda-psycopg2",
    version="0.0.1",
    url="https://github.com/simcoehsieh/aws-lambda-psycopg2/src",
    license='Proprietary',

    author="Simcoe",
    author_email="simcoe7816@gmail.com",

    description="A module that optimizes Redis memory usage by storing splits large hashes into multiple 'shards' that are stored as ziplists.",
    long_description=read("README.md"),

    packages=find_packages(exclude=('',)),
    package_data={'': ['_psycopg.cpython-36m-darwin.so', '_psycopg.cpython-36m-x86_64-linux-gnu.so']},

    install_requires=[],

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: Other/Proprietary License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
