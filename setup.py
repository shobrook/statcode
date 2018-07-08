from setuptools import find_packages
from setuptools import setup

setup(
    name="teen",
    description="Like man pages, but for HTTP status codes",
    version="v1.0.1",
    install_requires=["pyyaml", "urwid"],
    packages=["teen"],
    entry_points={"console_scripts": ["rebound = rebound.rebound:main"]},
    include_package_data=True,
    python_requires=">=3",
    url="https://github.com/shobrook/teen",
    author="shobrook",
    author_email="shobrookj@gmail.com",
    license="MIT"
)
