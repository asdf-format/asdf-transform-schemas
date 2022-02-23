"""
Script that creates initial transform manifests from the version_map
files in the asdf-standard repo.  This file can be removed once
the format of the manifest files has been finalized.
"""
import argparse

import asdf
import yaml


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("version_map_path")
    parser.add_argument("output_path")
    return parser.parse_args()


class MultilineString(str):
    pass


def represent_multiline_string(dumper, data):
    return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")


yaml.add_representer(MultilineString, represent_multiline_string)

args = parse_args()

asdf_standard_version = args.version_map_path.split("/")[-1].rsplit(".", 1)[0].split("-")[-1]

with open(args.version_map_path) as f:
    version_map = yaml.safe_load(f.read())

manifest = {}

manifest["id"] = f"http://stsci.edu/asdf/extensions/transform/manifests/transform-{asdf_standard_version}"
manifest["extension_uri"] = f"http://stsci.edu/asdf/extensions/transform-{asdf_standard_version}"
manifest["title"] = f"Transform extension {asdf_standard_version}"
manifest["description"] = MultilineString("A set of tags for serializing data transforms.")
manifest["tags"] = []

for tag_base, tag_version in version_map["tags"].items():
    if tag_base.startswith("tag:stsci.edu:asdf/transform/"):
        tag_uri = f"{tag_base}-{tag_version}"
        schema_uri = tag_uri.replace("tag:stsci.edu:asdf/transform/", "http://stsci.edu/schemas/asdf/transform/")
        schema = asdf.schema.load_schema(schema_uri)
        manifest["tags"].append(
            {
                "tag_uri": tag_uri,
                "schema_uri": schema_uri,
                "title": schema["title"].strip(),
                "description": MultilineString(schema["description"].strip()),
            }
        )

with open(args.output_path, "w") as f:
    yaml.dump(manifest, f, sort_keys=False)
