from asdf.extension import default_extensions, AsdfExtensionList
from asdf import generic_io
import yaml

from asdf_transform_schemas.extension import AsdfTransformSchemasExtension


def test_extension_registered():
    assert any(
        isinstance(e, AsdfTransformSchemasExtension)
        for e in default_extensions.extensions
    )


def test_resolver():
    extension_list = AsdfExtensionList([AsdfTransformSchemasExtension()])
    schema_id = "http://asdf-format.org/schemas/transform/add-2.0.0"

    url = extension_list.resolver(schema_id)

    with generic_io.get_file(url) as f:
        schema = yaml.safe_load(f.read())

    assert schema["id"] == schema_id
