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

    code = ""
    expected = None
    result = mapper.map(code)
    assert result is expected

    code = "A0224"
    expected = "00324"
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

    code = ["A0224",123, "A179", "", "812938"]
    expected = ["00324", None, "01790", None, None]
    result = mapper.map(code)
    assert result == expected