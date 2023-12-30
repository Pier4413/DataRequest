from setuptools import setup

setup(
    name='data_request',
    packages=['data_request'],
    description='A simple wrapper to make HTTP Requests',
    version='1.0.8',  # updated
    url='https://github.com/Pier4413/DataRequest',
    author='Panda',
    author_email='panda@delmasweb.net',
    install_requires=[
        'requests'
    ],
    keywords=['http', 'request', 'api']
)
