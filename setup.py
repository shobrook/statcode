try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
from codecs import open

setup(
    name="statcode",
    description="Like man pages, but for HTTP status codes",
    version="v1.0.0",
    install_requires=["pyyaml", "urwid"],
    packages=["statcode"],
    entry_points={"console_scripts": ["statcode = statcode.statcode:main"]},
    include_package_data=True,
    python_requires=">=3",
    url="https://github.com/shobrook/statcode",
    author="shobrook",
    author_email="shobrookj@gmail.com",
    license="MIT"
)
