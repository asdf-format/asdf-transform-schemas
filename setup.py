#!/usr/bin/env python
import os

from setuptools import setup


package_dir = {"": "src"}
packages = ["asdf_transform_schemas"]
for directory in ["schemas", "schema_collections"]:
    for walk_result in os.walk(directory):
        path = walk_result[0]
        package = ".".join(["asdf_transform_schemas"] + path.split(os.sep))
        package_dir[package] = path
        packages.append(package)

setup(use_scm_version=True, packages=packages, package_dir=package_dir)
