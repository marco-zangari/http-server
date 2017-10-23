from setuptools import setup

setup(
    name='http-server',
    package_dir={'': 'src'},
    py_modules=[],
    description='Server and client built with Python sockets',
    author='Megan Flood, Marco Zangari',
    author_email='mak.flood@comcast.net, mjzangari@gmail.com',
    install_requires=[],
    extras_require={'test': ['pytest', 'pytest-watch', 'pytest-cov', 'tox']}
)
