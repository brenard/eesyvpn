#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""EesyVPN python librairy"""


from setuptools import setup, find_packages


doc_lines = __doc__.split('\n')


setup(
    author=u'Benjamin Renard',
    author_email=u'brenard@zionetrix.net',
    description=doc_lines[0],
    include_package_data=True,
    long_description='\n'.join(doc_lines[2:]),
    name=u'EesyVPN',
    packages=find_packages(),
    version='0.1',
    zip_safe=False,
    )
