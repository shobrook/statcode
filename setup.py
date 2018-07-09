try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
from codecs import open

setup(
    name="teen",
    description="Like man pages, but for HTTP status codes",
    version="v1.0.3",
    install_requires=["pyyaml", "urwid"],
    packages=["teen"],
    entry_points={"console_scripts": ["teen = teen.teen:main"]},
    include_package_data=True,
    python_requires=">=3",
    url="https://github.com/shobrook/teen",
    author="shobrook",
    author_email="shobrookj@gmail.com",
    license="MIT"
)
