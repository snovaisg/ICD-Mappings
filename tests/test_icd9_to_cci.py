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

    code = ["20104", 123, "4613"]
    expected = [True, None, False]
    result = mapper.map(code)
    assert result == expected