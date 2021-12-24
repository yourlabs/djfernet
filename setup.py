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
    keywords='fernet cryptography django',
    python_requires='>=3.8',
    packages=['fernet_fields'],
)
