from pathlib import Path

import asdf
import pytest
import yaml


def get_resources():
    resources_root = Path(__file__).parent.parent / "resources"

    return {str(path.relative_to(resources_root)): path for path in resources_root.glob("**/*.yaml")}


RESOURCES = get_resources()


@pytest.mark.parametrize("resource", RESOURCES)
def test_resource(resource):
    resource_path = RESOURCES[resource]
    resource_manager = asdf.get_config().resource_manager

    with resource_path.open("rb") as f:
        resource_content = f.read()
    resource = yaml.safe_load(resource_content)
    resource_uri = resource["id"]
    assert resource_manager[resource_uri] == resource_content


def get_manifests():
    manifests_root = Path(__file__).parent.parent / "resources" / "asdf-format.org" / "manifests"

    return {str(path.relative_to(manifests_root)): path for path in manifests_root.glob("*.yaml")}



MANIFESTS = get_manifests()
LATEST_MANIFEST_FILE = sorted(MANIFESTS)[-1]


@pytest.fixture
def latest_manifest():
    with MANIFESTS[LATEST_MANIFEST_FILE].open("rb") as f:
        return yaml.safe_load(f.read())


@pytest.mark.parametrize("manifest_filename", MANIFESTS)
def test_manifest(manifest_filename):
    manifest_path = MANIFESTS[manifest_filename]
    resource_manager = asdf.get_config().resource_manager

    with manifest_path.open("rb") as f:
        manifest_content = f.read()
    manifest = yaml.safe_load(manifest_content)

    manifest_schema = asdf.schema.load_schema("asdf://asdf-format.org/core/schemas/extension_manifest-1.0.0")

    # The manifest must be valid against its own schema:
    asdf.schema.validate(manifest, schema=manifest_schema)

    for tag_definition in manifest["tags"]:
        # The tag's schema must be available:
        assert tag_definition["schema_uri"] in resource_manager

    assert manifest["id"].endswith(manifest_filename.strip(".yaml"))


# perform a few checks on the latest manifest (the only one that should change)

def test_manifest_tag_order(latest_manifest):
    """Tags should be sorted alphabetically"""
    tag_uris = [tag_def["tag_uri"] for tag_def in latest_manifest["tags"]]
    assert tag_uris == sorted(tag_uris)


def test_tags_match_schemas(latest_manifest):
    """Check that tag and schema versions match"""
    for tag_def in latest_manifest["tags"]:
        tag_uri = tag_def["tag_uri"]
        schema_uri = tag_def["schema_uri"]
        assert tag_uri.split(":")[-1] in schema_uri


def test_uses_latest_schemas(latest_manifest):
    """The latest manifest should always use the latest schemas"""
    for tag_def in latest_manifest["tags"]:
        schema_uri = tag_def["schema_uri"]
        base_uri = schema_uri.rsplit("-", maxsplit=1)[0]
        final_path = base_uri.rsplit("/", maxsplit=1)[-1]

        # find all schemas with this base_uri
        matches = []
        for resource in RESOURCES:
            if resource.rsplit("-", maxsplit=1)[0].rsplit("/", maxsplit=1)[-1] == final_path:
                matches.append(resource)

        # we should find at least 1 match
        assert matches

        # get the latest one
        latest_schema = sorted(matches)[-1]
        assert schema_uri.endswith(latest_schema.rsplit("/", maxsplit=1)[-1].rsplit(".", maxsplit=1)[0])
