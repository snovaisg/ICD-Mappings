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

    code = ""
    expected = None
    result = mapper.map(code)
    assert result is expected

    code = "123.45"
    expected = None
    result = mapper.map(code)
    assert result == expected

    code = "5352"
    expected = "140"
    result = mapper.map(code)
    assert result == expected

    code = 2.45
    expected = None
    result = mapper.map(code)
    assert result is expected

    # Test codes with dots - should work after dot stripping
    code = "53.52"
    expected = "140"  # same as "5352"
    result = mapper.map(code)
    assert result == expected

    code = "201.04"
    expected = "37"  # same as "20104"
    result = mapper.map(code)
    assert result == expected

    code = ["20104", 123, "4339", "", "918283818", "53.52"]
    expected = ["37", None, "110", None, None, "140"]  # "53.52" now maps correctly
    result = mapper.map(code)
    assert result == expected