from setuptools import setup, find_packages

setup(
    name='mytesseract',
    version='0.1.0',
    test_suite='nose.collector',
    tests_require=['nose'],
    packages=find_packages(include=[
        'tesstrain',
        'tesstest'
    ])
)
