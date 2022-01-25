#!/usr/bin/env python
from setuptools import setup, find_packages


packages = find_packages(where="src")
packages.append("asdf_transform_schemas.resources")

package_dir = {
    "": "src",
    "asdf_transform_schemas.resources": "resources",
}

package_data = {
    "asdf_transform_schemas.resources": ["*.yaml", "**/*.yaml", "**/**/*.yaml", "**/**/**/*.yaml"],
}

setup(
    use_scm_version=True,
    packages=packages,
    package_dir=package_dir,
    package_data=package_data,
)
