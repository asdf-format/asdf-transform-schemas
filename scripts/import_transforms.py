"""
Script that imports transform schemas from asdf-standard.
This file can be removed once the format of the new schemas
is finalized.
"""
import argparse
import glob
import os
import re

import pkg_resources

TAG_PATTERN = re.compile(r"^tag: .*?\n", re.MULTILINE | re.DOTALL)
ID_PATTERN = re.compile(r"^id: .*?/([^/-]+)-.*?\n", re.MULTILINE | re.DOTALL)
METASCHEMA_PATTERN = re.compile(r"^\$schema: .*?\n", re.MULTILINE | re.DOTALL)

# References to schemas outside of the transforms directory.
EXTERNAL_REF_PATTERN = re.compile(r'\$ref: "?\.\./(.*?[0-9]\.[0-9]\.[0-9])"?')

# Any $ref that hasn't been converted to an http URI by the
# previous regex will be a reference to another transform.
INTERNAL_REF_PATTERN = re.compile(r'\$ref: "?(?!http)(.*?)-[0-8]\.[0-9]\.[0-9]"?')

# These (found in the examples) will be updated to absolute tags:
BANG_TRANSFORM = re.compile(r"!transform/([^ \n-]*)-[^ \n]*")
BANG_UNIT = re.compile(r"!unit/([^ \n]*)")
BANG_CORE = re.compile(r"!core/([^ \n]*)")

# URI prefix (both id and tag) of new schemas.
URI_PREFIX = "http://asdf-format.org/schemas/transform"

# Initial version of new schemas.
VERSION = "2.0.0"

# For now just leave this at draft-01, but when we remove tag
# we'll need to bring in draft-02.
METASCHEMA = "http://stsci.edu/schemas/yaml-schema/draft-01"


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("source_path")
    parser.add_argument("dest_path")
    return parser.parse_args()


args = parse_args()


paths = list(glob.glob(os.path.join(args.source_path, "*.yaml")))
paths_by_name = {}
for path in paths:
    filename = os.path.basename(path)
    name = filename.split("-")[0]
    version = filename.split("-")[-1].rsplit(".", 1)[0]
    if name not in paths_by_name:
        paths_by_name[name] = []
    paths_by_name[name].append((path, version))


latest_paths = []
for name, name_paths in paths_by_name.items():
    latest_paths.append(sorted(name_paths, key=lambda p: pkg_resources.parse_version(p[-1]))[-1][0])


for path in latest_paths:
    with open(path) as f:
        content = f.read()

    filename = os.path.basename(path)
    new_filename = filename.split("-")[0] + f"-{VERSION}.yaml"

    schema_name = ID_PATTERN.search(content).group(1)
    new_uri = f"{URI_PREFIX}/{schema_name}-{VERSION}"

    new_id = f"id: {new_uri}\n"
    content = ID_PATTERN.sub(new_id, content)

    new_tag = f"tag: {new_uri}\n"
    content = TAG_PATTERN.sub(new_tag, content)

    content = METASCHEMA_PATTERN.sub(f"$schema: {METASCHEMA}\n", content)

    content = EXTERNAL_REF_PATTERN.sub(r"$ref: http://stsci.edu/schemas/asdf/\1", content)
    content = INTERNAL_REF_PATTERN.sub(rf"$ref: \1-{VERSION}", content)

    content = BANG_TRANSFORM.sub(rf"!<{URI_PREFIX}/\1-{VERSION}>", content)

    # TODO: Update these once core schemas start using http:// URIs:
    content = BANG_UNIT.sub(r"!<tag:stsci.edu:asdf/unit/\1>", content)
    content = BANG_CORE.sub(r"!<tag:stsci.edu:asdf/core/\1>", content)

    output_path = os.path.join(args.dest_path, new_filename)

    with open(output_path, "w") as f:
        f.write(content)
