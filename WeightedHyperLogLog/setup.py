from distutils.core import setup, Extension

setup(
    name='WHLL',
    version='0.0.1',
    description='Weighted HyperLogLog implementation in C for Python.',
    ext_modules=[
        Extension('WHLL', ['src/whll.c', 'lib/murmur2.c', ]),
        ],
    headers=['src/whll.h', 'lib/murmur2.h', ],
    )
