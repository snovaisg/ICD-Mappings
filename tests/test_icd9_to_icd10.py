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

    code = ""
    expected = None
    result = mapper.map(code)
    assert result is expected

    code = "123.45"
    expected = None
    result = mapper.map(code)
    assert result == expected

    code = "00863"
    expected = "A0811"
    result = mapper.map(code)
    assert result == expected

    code = "23b132"
    expected = None
    result = mapper.map(code)
    assert result == expected

    code = 2.45
    expected = None
    result = mapper.map(code)
    assert result is expected

    # Test codes with dots - should work after dot stripping
    code = "008.63"
    expected = "A0811"  # same as "00863"
    result = mapper.map(code)
    assert result == expected

    code = "04.02"
    expected = "K9081"  # same as "0402"
    result = mapper.map(code)
    assert result == expected

    code = ["00863", 123, "0402", "", "008.63"]
    expected = ["A0811", None, "K9081", None, "A0811"]  # "008.63" now maps to "A0811"
    result = mapper.map(code)
    assert result == expected