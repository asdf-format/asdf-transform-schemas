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

UNIT_TAGS = {"tag:stsci.edu:asdf/unit/unit-1.*", "tag:astropy.org:astropy/units/unit-1.*"}


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


@pytest.mark.parametrize("tag_set", (UNIT_TAGS,))
def test_tags_in_allof(latest_schema, tag_set):
    """
    Test that some tags (unit) where the
    tag used depends on the value are always referenced in an
    allof containing all tags.
    """
    # we walk_and_modify here to use postorder

    def callback(node):
        if not isinstance(node, dict):
            return node
        if "anyOf" in node:
            # check if this anyof includes a tag in the set
            seen = set()
            for sub in node["anyOf"]:
                if not isinstance(sub, dict):
                    continue
                if "tag" not in sub:
                    continue
                if sub["tag"] in tag_set:
                    seen.add(sub["tag"])

            if seen:
                # if a tag was found, check both were found
                assert seen == tag_set, f"anyOf {node} missing: {tag_set - seen}"
                # remove the anyof so the code below can check for tags not in the anyof
                return {k: v for k, v in node.items() if k != "anyOf"}
        if tag := node.get("tag"):
            assert tag not in tag_set, f"tag {tag} must be in an anyOf with: {tag_set}"
        return node

    asdf.treeutil.walk_and_modify(latest_schema, callback, postorder=False)
