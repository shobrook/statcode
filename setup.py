try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
from codecs import open

setup(
    name="httphelp",
    description="Like man pages, but for HTTP status codes and headers (and more)",
    version="v1.1.0",
    install_requires=["pyyaml", "urwid"],
    packages=["statcode"],
    entry_points={"console_scripts": ["httphelp = statcode.statcode:main"]},
    include_package_data=True,
    python_requires=">=3",
    url="https://github.com/Malex/statcode",
    author="Malex",
    author_email="malexprojects@gmail.com",
    license="MIT"
)
