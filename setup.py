from setuptools import setup
from data_request.metadata.__version__ import __version__
setup(
    name='data_request',
    packages=['data_request'],
    description='A simple wrapper to make HTTP Requests',
    version=__version__,  # updated
    url='https://github.com/Pier4413/DataRequest',
    author='Panda',
    author_email='panda@delmasweb.net',
    install_requires=[
        'requests'
    ],
    keywords=['http', 'request', 'api']
)
