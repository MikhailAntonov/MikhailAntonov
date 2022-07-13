from setuptools import setup, find_packages

setup(
    name="classic-ml-train-tools",
    version="0.0.1",
    author="Mikhail Antonov",
    author_email="mikhail.antonoff@gmail.com",
    description="Some of classic ML train tools",
    packages=find_packages(),
    install_requires=[
        "scikit_learn==1.0.2",
        "numpy==1.22.1",
        "pandas==1.4.0",
        "sqlalchemy==1.4.18",
        "pyhive[presto]==0.6.5",
        "presto-python-client==0.8.2",
        "pyod==1.0.0",
        "catboost==0.24.2",
        "kafka-python==2.0.2",
        "marshmallow-dataclass==8.5.3",
        "geopy==1.21.0",
    ],
)
