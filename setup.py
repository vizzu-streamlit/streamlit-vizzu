from pathlib import Path

import setuptools

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setuptools.setup(
    name="streamlit-vizzu",
    version="0.1.6",
    author="Zachary Blackwoood",
    author_email="zachary@streamlit.io",
    description=(
        "Bidirectional streamlit component for interacting with vizzu animations"
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    classifiers=[],
    python_requires=">=3.7",
    install_requires=["streamlit>=1.13.0", "ipyvizzu>=0.15.0,<0.17.0"],
)
