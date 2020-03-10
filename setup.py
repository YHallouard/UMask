from setuptools import setup, find_packages

setup(name='UMask',
      version='1.0',
      description='This Package is a contribution to shapely and imantics. It provides you with a function to convert \
      Mask pictures into their WKT representation and another to create Mask from WKT object.',
      url='',
      author='Yann Hallouard',
      author_email='',
      license='',
      packages=find_packages(),
      install_requires=['pandas', 'numpy', 'shapely', 'imantics', 'tqdm', 'Pillow', 'pytest'],
      test_suite='nose.collector',
      tests_require=['nose'],
      zip_safe=False)
