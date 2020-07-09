from pathlib import Path

import asdf
import yaml


def test_schemas():
    schemas_root = Path(__file__).parent.parent / "schemas"
    resource_manager = asdf.get_config().resource_manager

    for schema_path in schemas_root.glob("*.yaml"):
        with schema_path.open("rb") as f:
            schema_content = f.read()
        schema = yaml.safe_load(schema_content)
        schema_uri = schema["id"]
        assert resource_manager[schema_uri] == schema_content
