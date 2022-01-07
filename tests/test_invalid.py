import pytest
import asdf
from asdf.tests import helpers


purposefully_failing = [
    # bounding_box fails
    """!transform/bounding_box-1.0.0
  [1.0, test]
    """,
    """!transform/bounding_box-1.0.0
  [1.0]
    """,
    """!transform/bounding_box-1.0.0
  [1.0, 2.0, 3.0]
    """,
    """!transform/bounding_box-1.0.0
  - [1.0, 2.0]
    """,
    """!transform/bounding_box-1.0.0
  - [1.0, 2.0]
  - [1.0, 2.0, 3.0]
    """,
    """!transform/bounding_box-1.0.0
  - [1.0, 2.0]
  - [1.0, test]
    """,
    """!transform/bounding_box-1.0.0
  - [1.0]
  - [1.0, 2.0]
    """,
    # compound_bounding_box fails
    """!transform/compound_bounding_box-1.0.0
  selector_args:
    - argument: x
  cbbox:
    - key: [0]
      bbox: [1.0, 2.0]
    """,
    """!transform/compound_bounding_box-1.0.0
  selector_args:
    - ignored: true
  cbbox:
    - key: [0]
      bbox: [1.0, 2.0]
    """,
    """!transform/compound_bounding_box-1.0.0
  selector_args:
    - argument: 5
    - ignored: true
  cbbox:
    - key: [0]
      bbox: [1.0, 2.0]
    """,
    """!transform/compound_bounding_box-1.0.0
  selector_args:
    - argument: x
      ignored: test
  cbbox:
    - key: [0]
      bbox: [1.0, 2.0]
    """,
    """!transform/compound_bounding_box-1.0.0
  selector_args: []
  cbbox:
    - key: [0]
      bbox: [1.0, 2.0]
    """,
    """!transform/compound_bounding_box-1.0.0
  selector_args:
    - argument: x
      ignored: true
  cbbox:
    - key: []
      bbox: [1.0, 2.0]
    """,
    """!transform/compound_bounding_box-1.0.0
  selector_args:
    - argument: x
      ignored: true
  cbbox:
    - key: [test]
      bbox: [1.0, 2.0]
    """,
    """!transform/compound_bounding_box-1.0.0
  selector_args:
    - argument: x
      ignored: true
  cbbox:
    - bbox: [1.0, 2.0]
    """,
    """!transform/compound_bounding_box-1.0.0
  selector_args:
    - argument: x
      ignored: true
  cbbox:
    - key: [0]
      bbox: [1.0, 2.0, 3.0]
    """,
    """!transform/compound_bounding_box-1.0.0
  selector_args:
    - argument: x
      ignored: true
  cbbox:
    - key: [0]
    """,
    """!transform/compound_bounding_box-1.0.0
  selector_args:
    - argument: x
      ignored: true
  cbbox: []
    """,
    """!transform/compound_bounding_box-1.0.0
  cbbox:
    - key: [0]
      bbox: [1.0, 2.0]
    """,
    """!transform/compound_bounding_box-1.0.0
  selector_args:
    - argument: x
      ignored: true
    """,
    # transform fails (both bounding_box and compound_bounding_box)
    """!transform/transform-1.2.0
  name: test
  bounding_box: [1.0, 2.0]
  compound_bounding_box:
    selector_args:
      - argument: x
        ignored: true
    cbbox:
      - key: [0]
        bbox: [1.0, 2.0]
    """,
]


@pytest.mark.parametrize("yaml", purposefully_failing)
def test_failing_schema(yaml):
    buff = helpers.yaml_to_asdf(f"example: {yaml.strip()}")
    with pytest.raises(asdf.ValidationError, match=r"Failed validating *"):
        asdf.open(buff)
