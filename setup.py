from setuptools import setup


setup(
    name='djfernet',
    versioning='dev',
    setup_requires='setupmeta',
    install_requires=[
        'cryptography',
        "Django>=3.2"
    ],
    author='James Pic',
    author_email='jamespic@gmail.com',
    url='https://yourlabs.io/oss/djfernet',
    include_package_data=True,
    license='MIT',
    keywords='fernet cryptography django',
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 3.2",
        "Framework :: Django :: 4.1",
        "Framework :: Django :: 4.2",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11"
    ],
    python_requires='>=3.8',
    packages=['fernet_fields'],
)
