import pytest
import asdf
from asdf.tests import helpers


purposefully_failing = [
    # old-style bounding box fails
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
    # 2D only one intervals
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
    # new-style bounding box fails
    # Missing intervals
    """!transform/shift-1.2.0
  offset: 1
  bounding_box:
    ignore: [x, y]
    order: C
    """,
    # No intervals
    """!transform/shift-1.2.0
  offset: 1
  bounding_box:
    intervals: {}
    ignore: [x, y]
    order: C
    """,
    # Bad interval
    """!transform/shift-1.2.0
  offset: 1
  bounding_box:
    intervals:
      x: [1.0, 2.0, 3.0]
    ignore: [x, y]
    order: C
    """,
    # Non-string ignore
    """!transform/shift-1.2.0
  offset: 1
  bounding_box:
    intervals:
      x: [1.0, 2.0]
    ignore: [x, y, 3]
    order: C
    """,
    # Order is not F or C
    """!transform/shift-1.2.0
  offset: 1
  bounding_box:
    intervals:
      x: [1.0, 2.0]
    ignore: [x, y]
    order: test
    """,
    # compound bounding box fails
    # missing ignore in selector
    """!transform/shift-1.2.0
  offset: 1
  bounding_box:
    selector_args:
      - argument: x
    cbbox:
      - key: [0]
        bbox:
          intervals:
            y: [1.0, 2.0]
    """,
    # missing argument in selector
    """!transform/shift-1.2.0
  offset: 1
  bounding_box:
    selector_args:
      - ignore: true
    cbbox:
      - key: [0]
        bbox:
          intervals:
            y: [1.0, 2.0]
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
        bbox:
          intervals:
            y: [1.0, 2.0]
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
        bbox:
          intervals:
            y: [1.0, 2.0]
    """,
    # Nothing in selector_args array
    """!transform/shift-1.2.0
  offset: 1
  bounding_box:
    selector_args: []
    cbbox:
      - key: [0]
        bbox:
          intervals:
            y: [1.0, 2.0]
    """,
    # Missing selector_args array
    """!transform/shift-1.2.0
  offset: 1
  bounding_box:
    cbbox:
      - key: [0]
        bbox:
          intervals:
            y: [1.0, 2.0]
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
        bbox:
          intervals:
            y: [1.0, 2.0]
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
        bbox:
          intervals:
            y: [1.0, 2.0]
    """,
    # Missing key entry
    """!transform/shift-1.2.0
  offset: 1
  bounding_box:
    selector_args:
      - argument: x
        ignore: true
    cbbox:
      - bbox:
          intervals:
            y: [1.0, 2.0]
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
        bbox:
          intervals:
            y: [1.0, 2.0, 3.0]
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
