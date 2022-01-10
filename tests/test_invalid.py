import pytest
import asdf
from asdf.tests import helpers


purposefully_failing = [
    # bounding_box fails
    # 1D string bound
    """!transform/shift-1.2.0
  offset: 1
  bounding_box: [1.0, test]
    """,
    # 1D only one bound
    """!transform/shift-1.2.0
  offset: 1
  bounding_box: [1.0]
    """,
    # 1D more than two bounds
    """!transform/shift-1.2.0
  offset: 1
  bounding_box: [1.0, 2.0, 3.0]
    """,
    # 2D only one interval
    """!transform/shift-1.2.0
  offset: 1
  bounding_box:
    - [1.0, 2.0]
    """,
    # 2D string bound
    """!transform/shift-1.2.0
  offset: 1
  bounding_box:
    - [1.0, 2.0]
    - [3.0, test]
    """,
    # 2D only one bound
    """!transform/shift-1.2.0
  offset: 1
  bounding_box:
    - [1.0, 2.0]
    - [3.0]
    """,
    # 2D more than two bounds
    """!transform/shift-1.2.0
  offset: 1
  bounding_box:
    - [1.0, 2.0]
    - [3.0, 4.0, 5.0]
    """,
    # bounding_box fails
    # missing ignore in selector
    """!transform/shift-1.2.0
  offset: 1
  bounding_box:
    selector_args:
      - argument: x
    cbbox:
      - key: [0]
        bbox: [1.0, 2.0]
    """,
    # missing argument in selector
    """!transform/shift-1.2.0
  offset: 1
  bounding_box:
    selector_args:
      - ignore: true
    cbbox:
      - key: [0]
        bbox: [1.0, 2.0]
    """,
    # argument is not a string
    """!transform/shift-1.2.0
  offset: 1
  bounding_box:
    selector_args:
      - argument: 5
        ignore: true
    cbbox:
      - key: [0]
        bbox: [1.0, 2.0]
    """,
    # ignore is not a boolean
    """!transform/shift-1.2.0
  offset: 1
  bounding_box:
    selector_args:
      - argument: x
        ignore: test
    cbbox:
      - key: [0]
        bbox: [1.0, 2.0]
    """,
    # Nothing in selector_args array
    """!transform/shift-1.2.0
  offset: 1
  bounding_box:
    selector_args: []
    cbbox:
      - key: [0]
        bbox: [1.0, 2.0]
    """,
    # Missing selector_args array
    """!transform/shift-1.2.0
  offset: 1
  bounding_box:
    cbbox:
      - key: [0]
        bbox: [1.0, 2.0]
    """,
    # Nothing in key array
    """!transform/shift-1.2.0
  offset: 1
  bounding_box:
    selector_args:
      - argument: x
        ignore: true
    cbbox:
      - key: []
        bbox: [1.0, 2.0]
    """,
    # Non-numeric key entry
    """!transform/shift-1.2.0
  offset: 1
  bounding_box:
    selector_args:
      - argument: x
        ignore: true
    cbbox:
      - key: [test]
        bbox: [1.0, 2.0]
    """,
    # Missing key entry
    """!transform/shift-1.2.0
  offset: 1
  bounding_box:
    selector_args:
      - argument: x
        ignore: true
    cbbox:
      - bbox: [1.0, 2.0]
    """,
    # Invalid bbox entry
    """!transform/shift-1.2.0
  offset: 1
  bounding_box:
    selector_args:
      - argument: x
        ignore: true
    cbbox:
      - key: [0]
        bbox: [1.0, 2.0, 3.0]
    """,
    # Missing bbox entry
    """!transform/shift-1.2.0
  offset: 1
  bounding_box:
    selector_args:
      - argument: x
        ignore: true
    cbbox:
      - key: [0]
    """,
    # Empty cbbox array
    """!transform/shift-1.2.0
  offset: 1
  bounding_box:
    selector_args:
      - argument: x
        ignore: true
    cbbox: []
    """,
    # Missing cbbox entry
    """!transform/shift-1.2.0
  offset: 1
  bounding_box:
    selector_args:
      - argument: x
        ignore: true
    """,
]


@pytest.mark.parametrize("yaml", purposefully_failing)
def test_failing_schema(yaml):
    buff = helpers.yaml_to_asdf(f"example: {yaml.strip()}")
    with pytest.raises(asdf.ValidationError, match=r"Failed validating *"):
        asdf.open(buff)
