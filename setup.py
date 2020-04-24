from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

required = ['imantics>=0.1.12',
            'numpy',
            'pandas',
            'Pillow>=7.0.0',
            'rasterio>=1.1.3',
            'Shapely>=1.7.0',
            'tqdm>=4.43.0']

setup(
    name='UMask',
    packages=find_packages(),
    version='2.0.1',
    description='This Package is a contribution to shapely and imantics. It provides you with a function to convert \
    Mask pictures into their WKT representation and another to create Mask from WKT object.',
    author='Yann Hallouard',
    long_description=long_description,
    long_description_content_type="text/markdown",
    setup_requires=['pytest-runner', 'wheel'],
    tests_require=required,
    install_requires=required,
    license='',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
