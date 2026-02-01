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

    # Test codes with dots - should work after dot stripping
    code = "A02.24"
    expected = "00324"  # same as "A0224"
    result = mapper.map(code)
    assert result == expected

    code = "A1.79"
    expected = "01790"  # same as "A179"
    result = mapper.map(code)
    assert result == expected

    code = ["A0224", 123, "A179", "", "812938", "A02.24"]
    expected = ["00324", None, "01790", None, None, "00324"]  # "A02.24" now maps correctly
    result = mapper.map(code)
    assert result == expected