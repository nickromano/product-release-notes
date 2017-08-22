from setuptools import setup, find_packages


DESCRIPTION = "Release notes page for your product."


setup(
    name="product_release_notes",
    version="0.0.8",
    url='https://github.com/nickromano/product-release-notes',
    license='BSD',
    description=DESCRIPTION,
    long_description=DESCRIPTION,
    author='Nick Romano',
    author_email='nick.r.romano@gmail.com',
    packages=find_packages(),
    package_data={'product_release_notes': ['templates/release_notes/*.html']},
    install_requires=[
        'Django>=1.8',
        'requests',
    ],
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    tests_require=[
        'mock'
    ],
    test_suite='testrunner.runtests'
)
