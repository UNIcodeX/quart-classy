"""
Quart-Classy
-------------

Class based views for Quart
"""
from setuptools import setup

setup(
    name='Quart-Classy',
    version='0.0.1',
    url='https://github.com/unicodex/quart-classy',
    license='BSD',
    author='Jared Fields',
    author_email='jbcomps@gmail.com',
    description='Class based views for Quart',
    long_description=__doc__,
    py_modules=['quart_classy'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Quart'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    test_suite='test_classy'
)