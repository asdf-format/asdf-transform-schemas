import re

import asdf

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

ASDF_QUANTITY_TAG = "tag:stsci.edu:asdf/unit/quantity-1.*"
ASTROPY_QUANTITY_TAG = "tag:astropy.org:astropy/units/quantity-1.*"
QUANTITY_TAGS = {ASDF_QUANTITY_TAG, ASTROPY_QUANTITY_TAG}


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


def test_quantity_tag(latest_schema):
    # we walk_and_modify here to use postorder

    def callback(node):
        if not isinstance(node, dict):
            return node
        if "anyOf" in node:
            # check if this anyof includes tag: quantity
            seen = set()
            for sub in node["anyOf"]:
                if not isinstance(sub, dict):
                    continue
                if "tag" not in sub:
                    continue
                if sub["tag"] in QUANTITY_TAGS:
                    seen.add(sub["tag"])

            if seen:
                # if a tag: quantity was found, check both were found
                assert seen == QUANTITY_TAGS, f"anyOf {node} missing: {QUANTITY_TAGS - seen}"
                # remove the anyof so the code below can check for quantity
                # tags not in anyof
                return {k: v for k, v in node.items() if k != "anyOf"}
        if tag := node.get("tag"):
            assert (
                tag not in QUANTITY_TAGS
            ), f"quantity tag {tag} must be in an anyOf with all quantity tags: {QUANTITY_TAGS}"
        return node

    asdf.treeutil.walk_and_modify(latest_schema, callback, postorder=False)
