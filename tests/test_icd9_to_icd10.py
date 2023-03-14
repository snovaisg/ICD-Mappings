import numpy as np
import pandas as pd

def test_import():
    from icdmappings.mappers import ICD9toICD10
    return

def test_init():
    from icdmappings.mappers import ICD9toICD10
    mapper = ICD9toICD10()
    return 

def test_mapper():
    from icdmappings.mappers import ICD9toICD10
    mapper = ICD9toICD10()

    code = "00863"
    expected = "A0811"
    result = mapper.map(code)
    assert result == expected

    code = "23b132"
    expected = None
    result = mapper.map(code)
    assert result == expected

    code = 2.45
    try:
        result = mapper.map(code)
    except TypeError:
        pass

    code = ["00863",123, "0402"]
    expected = ["A0811", None, "K9081"]
    result = mapper.map(code)
    assert result == expected

    code = pd.Series(["00863",123, "0402"])
    expected = pd.Series(["A0811", None, "K9081"],index=code.index)
    result = mapper.map(code)
    assert result.equals(expected)

    code = np.array(["00863",123, "0402"])
    expected = np.array(["A0811", None, "K9081"])
    result = mapper.map(code)
    assert np.array_equal(result,expected)
