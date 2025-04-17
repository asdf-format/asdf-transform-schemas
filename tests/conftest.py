from pathlib import Path

import pytest
import yaml


def get_latest_schema_uris(resource_paths):
    by_base_uri = {}
    for resource_path in resource_paths:
        # skip manifests
        if "manifests" in resource_path.parts:
            continue

        # get uri from schema id
        with resource_path.open("rb") as f:
            schema_uri = yaml.safe_load(f.read())["id"]

        # get base uri and version
        base, version = schema_uri.rsplit("-", maxsplit=1)
        if base not in by_base_uri:
            by_base_uri[base] = {}
        by_base_uri[base][version] = schema_uri
    return [by_version[max(by_version.keys())] for _, by_version in by_base_uri.items()]


RESOURCE_PATHS = list((Path(__file__).parent.parent / "resources").glob("**/*.yaml"))
MANIFEST_PATHS = [p for p in RESOURCE_PATHS if "manifests" in p.parts]
LATEST_SCHEMA_URIS = get_latest_schema_uris(RESOURCE_PATHS)


@pytest.fixture(params=RESOURCE_PATHS)
def resource_path(request):
    yield request.param


@pytest.fixture(params=MANIFEST_PATHS)
def manifest_path(request):
    yield request.param


@pytest.fixture
def latest_manifest_path():
    yield max(MANIFEST_PATHS)


@pytest.fixture
def latest_manifest(latest_manifest_path):
    with latest_manifest_path.open("rb") as f:
        yield yaml.safe_load(f.read())


@pytest.fixture
def latest_schema_uris():
    yield LATEST_SCHEMA_URIS
