import numpy as np
import pandas as pd

def test_import():
    from icdmappings.mappers import ICD10toICD9
    return

def test_init():
    from icdmappings.mappers import ICD10toICD9
    mapper = ICD10toICD9()
    return 

def test_mapper():
    from icdmappings.mappers import ICD10toICD9
    mapper = ICD10toICD9()

    code = "A0224"
    expected = "00324"
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

    code = ["A0224",123, "A179"]
    expected = ["00324", None, "01790"]
    result = mapper.map(code)
    assert result == expected

    code = pd.Series(["A0224",123, "A179"])
    expected = pd.Series(["00324", None, "01790"],index=code.index)
    result = mapper.map(code)
    assert result.equals(expected)

    code = np.array(["A0224",123, "A179"])
    expected = np.array(["00324", None, "01790"])
    result = mapper.map(code)
    assert np.array_equal(result,expected)
