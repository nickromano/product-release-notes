from setuptools import setup

DESCRIPTION = "Release notes page for your product."


setup(
    name="product_release_notes",
    version="0.0.1",
    url='https://github.com/nickromano/product-release-notes',
    license='BSD',
    description=DESCRIPTION,
    long_description=DESCRIPTION,
    author='Nick Romano',
    author_email='nick.r.romano@gmail.com',
    packages=['product_release_notes'],  # , 'product_release_notes.migrations'],
    install_requires=[
        'Django>=1.8',
    ],
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    tests_require=[
    ],
    test_suite='testrunner.runtests'
)
