from setuptools import setup, find_packages

setup(
    name='fudosan_ai',
    description='Japanese real estate price predictors',
    author='Gary Sentosa',
    author_email='gary.sentosa@gmail.com',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
)
