from setuptools import setup, find_packages

setup(
    name='fudosan_ai',
    description='Japanese real estate price predictors',
    author='Gary Sentosa',
    author_email='gary.sentosa@gmail.com',
    packages=['app'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "Flask==1.1.2,",
        "numpy==1.19.1,",
        "pandas==1.0.5,",
        "python-dateutil==2.8.1,",
        "pymongo==3.11.2",
        "scikit-learn==0.23.2,",
    ],
)
