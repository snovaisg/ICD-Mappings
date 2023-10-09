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

    code = ["00863",123, "0402", "", "008.63"]
    expected = ["A0811", None, "K9081", None, None]
    result = mapper.map(code)
    assert result == expected