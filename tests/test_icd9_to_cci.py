def test_import():
    from icdmappings.mappers import ICD9toCCI
    return

def test_init():
    from icdmappings.mappers import ICD9toCCI
    mapper = ICD9toCCI()
    return 

def test_mapper():
    from icdmappings.mappers import ICD9toCCI
    mapper = ICD9toCCI()

    code = ""
    expected = None
    result = mapper.map(code)
    assert result is expected

    code = "9990"
    expected = False 
    result = mapper.map(code)
    assert result == expected

    code = '5679'
    expected = False
    result = mapper.map(code)
    assert result == expected

    code = "V450"
    expected = True
    result = mapper.map(code)
    assert result == expected

    code = 2.45
    expected = None
    result = mapper.map(code)
    assert result is expected

    # Test codes with dots - should work after dot stripping
    code = "999.0"
    expected = False  # same as "9990"
    result = mapper.map(code)
    assert result == expected

    code = "V45.0"
    expected = True  # same as "V450"
    result = mapper.map(code)
    assert result == expected

    code = ["20104", 123, "4613", "999.0", "V45.0"]
    expected = [True, None, False, False, True]  # dotted codes now map correctly
    result = mapper.map(code)
    assert result == expected