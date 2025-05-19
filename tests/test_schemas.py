import re

import asdf

import pytest

ALLOWED_REFS = (
    r"^transform-[0-9.]+$",
    r"^conic-[0-9.]+$",
    r"^cylindrical-[0-9.]+$",
    r"^pseudoconic-[0-9.]+$",
    r"^pseudocylindrical-[0-9.]+$",
    r"^quadcube-[0-9.]+$",
    r"^zenithal-[0-9.]+$",
    r"^#.*$",
)


def test_only_known_refs(latest_schema):
    """Latest schemas should only contain specific refs"""
    for node in asdf.treeutil.iter_tree(latest_schema):
        if not isinstance(node, dict):
            continue
        if "$ref" in node:
            uri = node["$ref"]
            if not any(re.match(pattern, uri) for pattern in ALLOWED_REFS):
                assert False, f"Unexpected $ref: {uri}"


def test_wildcard_tags(latest_schema):
    """Latest schemas should only contain wildcarded tags"""
    for node in asdf.treeutil.iter_tree(latest_schema):
        if not isinstance(node, dict):
            continue
        if "tag" in node:
            pattern = node["tag"]
            if "*" not in pattern:
                assert False, f"tag pattern missing wildcard: {pattern}"
