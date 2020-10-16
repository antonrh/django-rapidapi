import os

from setuptools import setup

root_path = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(root_path, "README.md")) as f:
    README = f.read()

EXTRAS_REQUIRE = {
    "tests": [
        "pytest>=6.1.1,<7.0.0",
        "pytest-cov>=2.10.1,<2.11.0",
        "pytest-django>=4.0.0,<4.1.0",
    ],
    "lint": [
        "mypy>=0.790,<1.0",
        "flake8>=3.8.4,<3.9.0",
        "isort>=5.6.4,<6.0.0",
        "black>=20.8b1,<20.9",
        "safety>=1.9.0,<1.10.0",
    ],
    "docs": [
        "mkdocs>=1.1.2,<1.2.0",
        "mkdocs-material>=6.0.2,<6.1.0",
    ],
}

EXTRAS_REQUIRE["dev"] = (
    EXTRAS_REQUIRE["tests"] + EXTRAS_REQUIRE["lint"] + EXTRAS_REQUIRE["docs"]
)

setup(
    name="django-rapidapi",
    version="0.1.0-dev1",
    description="",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Anton Ruhlov",
    author_email="antonruhlov@gmail.com.com",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    packages=["rapidapi"],
    package_data={"rapidapi": ["py.typed"]},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "django>=3.1,<3.2",
        "pydantic>=1.6.1,<1.7.0",
    ],
    extras_require=EXTRAS_REQUIRE,
)
