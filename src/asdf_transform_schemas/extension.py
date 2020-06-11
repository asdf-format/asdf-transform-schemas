import os
from urllib.request import pathname2url, urljoin


_PACKAGE_ROOT = os.path.abspath(os.path.dirname(__file__))


def _locate_directory(name):
    # Ordinary install:
    path = os.path.join(_PACKAGE_ROOT, name)
    if os.path.exists(path):
        return path

    # Editable install:
    path = os.path.abspath(os.path.join(_PACKAGE_ROOT, "..", "..", name))
    if os.path.exists(path):
        return path

    raise RuntimeError(f"Unable to locate {name} directory")


_SCHEMAS_ROOT_URL = urljoin("file:", pathname2url(_locate_directory("schemas")))


class AsdfTransformSchemasExtension:
    @property
    def types(self):
        return []

    @property
    def tag_mapping(self):
        # In these schemas, the tag and the id properties have
        # the same value, so no mapping is required.
        return []

    @property
    def url_mapping(self):
        return [
            (
                "http://asdf-format.org/schemas/transform/",
                _SCHEMAS_ROOT_URL + "/{url_suffix}.yaml",
            )
        ]
