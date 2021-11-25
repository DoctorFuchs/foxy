from sys import version
from setuptools import setup, find_packages
import datetime

version = datetime.date.today().strftime("%Y.%m.%d")

setup(
    package_dir= {"":"src"},
    packages= find_packages("src"),
    version=version
)