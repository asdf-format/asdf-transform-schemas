from pathlib import Path
import sys

if sys.version_info < (3, 9):
    import importlib_resources
else:
    import importlib.resources as importlib_resources

from asdf.resource import DirectoryResourceMapping

import asdf_transform_schemas


def get_resource_mappings():
    schemas_root = importlib_resources.files(asdf_transform_schemas) / "schemas"
    if not schemas_root.is_dir():
        # In an editable install, the schemas directory will exist off the
        # repository root:
        schemas_root = Path(__file__).parent.parent.parent / "schemas"
        if not schemas_root.is_dir():
            raise RuntimeError("Missing schemas directory")

    return [
        DirectoryResourceMapping(
            schemas_root, "http://asdf-format.org/schemas/transform"
        )
    ]
