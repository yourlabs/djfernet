from setuptools import setup


setup(
    name='djfernet',
    versioning='dev',
    setup_requires='setupmeta',
    install_requires=['cryptography'],
    author='James Pic',
    author_email='jamespic@gmail.com',
    url='https://yourlabs.io/oss/djfernet',
    include_package_data=True,
    license='MIT',
    keywords='cli',
    python_requires='>=3.8',
    entry_points={
        'console_scripts': [
            'cli2 = cli2.cli:main.entry_point',
        ],
    },
)
