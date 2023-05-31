from setuptools import find_packages, setup
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="unu",
    version="0.0.1",
    description="A Django app that makes life with Django a bit more enjoyable",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Danijel Pancic",
    author_email="danijel.pancic@unuaondo.com",
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3 :: Only",
    ],
    keywords="development, utilities, utils",
    include_package_data=True,
    packages=find_packages(),
    python_requires=">=3.10, <4",
    install_requires=[
        "django",
        "gunicorn",
        "psycopg2-binary",
        "python3-memcached",
        "requests",
        "beautifulsoup4",
        "html5lib",
        "lxml",
        "pymongo",
        "pycryptodomex",
        "whoosh",
        "pyjwt",
        "pyyaml",
        "yamlordereddictloader",
        "calmjs.parse",
        "black",
        "isort",
        "autoflake",
    ],
    project_urls={
        "Bug Reports": "https://git.unuaondo.com/danijel.pancic/djangoutils/-/issues",
        "Source": "https://git.unuaondo.com/danijel.pancic/djangoutils",
    },
)
