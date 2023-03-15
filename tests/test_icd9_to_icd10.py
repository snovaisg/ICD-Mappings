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