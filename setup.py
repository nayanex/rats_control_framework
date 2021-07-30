from os import getenv

from setuptools import setup


def get_required_packages():
    with open("requirements.txt") as f:
        return f.read().splitlines()


setup(
    name="abnamro_rats_controlframework",
    version="0.0.1",
    packages=[""],
    package_dir={"": "src"},
    author="Dmytro Shyshov",
    author_email="dmytro.shyshov@nl.abnamro.com",
    python_requires=">=3.7",
    description="Automated generation of evidences",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
)

setup(version=getenv("STPL_APPLICATION_VERSION"))
