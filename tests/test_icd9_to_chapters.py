import numpy as np
import pandas as pd

def test_import():
    from icdmappings.mappers import ICD9toChapters
    return

def test_init():
    from icdmappings.mappers import ICD9toChapters
    mapper = ICD9toChapters()
    return 

def test_mapper():
    from icdmappings.mappers import ICD9toChapters
    mapper = ICD9toChapters()


    code = "999"
    expected = "17" 
    result = mapper.map(code)
    assert result == expected

    code = "5352"
    expected = "9"
    result = mapper.map(code)
    assert result == expected

    code = 2.45
    try:
        result = mapper.map(code)
    except TypeError:
        pass

    code = ["20104",123, "4339"]
    expected = ["2", None, "7"]
    try:
        result = mapper.map(code)
    except TypeError:
        pass

    code = pd.Series(["20104","123", "4339"])
    expected = pd.Series(["2", "1", "7"],index=code.index)
    result = mapper.map(code)
    assert result.equals(expected)

    code = np.array(["20104","123", "4339"])
    expected = np.array(["2", "1", "7"])
    result = mapper.map(code)
    assert np.array_equal(result,expected)

    # edge cases
    code = "15268176283765123123"
    expected = None
    will_get = mapper.map("152")
    result = mapper.map(code)
    assert will_get == result