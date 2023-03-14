import numpy as np
import pandas as pd

def test_import():
    from icdmappings.mappers import ICD9toCCS
    return

def test_init():
    from icdmappings.mappers import ICD9toCCS
    mapper = ICD9toCCS()
    return 

def test_mapper():
    from icdmappings.mappers import ICD9toCCS
    mapper = ICD9toCCS()

    code = "123.45"
    expected = None
    result = mapper.map(code)
    assert result == expected

    code = "5352"
    expected = "140"
    result = mapper.map(code)
    assert result == expected

    code = 2.45
    try:
        result = mapper.map(code)
    except TypeError:
        pass

    code = ["20104",123, "4339"]
    expected = ["37", None, "110"]
    result = mapper.map(code)
    assert result == expected

    code = pd.Series(["20104",123, "4339"])
    expected = pd.Series(["37", None, "110"],index=code.index)
    result = mapper.map(code)
    assert result.equals(expected)

    code = np.array(["20104",123, "4339"])
    expected = np.array(["37", None, "110"])
    result = mapper.map(code)
    assert np.array_equal(result,expected)
