import pandas as pd
import numpy as np

def test_icd9_validator_import():
    from icdmappings.validators import ICD9Validator
    return

def test_icd9_validator_init():
    from icdmappings.validators import ICD9Validator
    validator = ICD9Validator()
    return 

def test_icd9_validator_validate_diagnostics():
    from icdmappings.validators import ICD9Validator
    validator = ICD9Validator()

    code = 3
    try:
        result = validator.validate_diagnostics(code)
    except TypeError as e:
        pass

    code = 'abc'
    expected = False
    result = validator.validate_diagnostics(code)
    assert result == expected

    code = '0760'
    expected = True
    result = validator.validate_diagnostics(code)
    assert result == expected

    code = None
    expected = None
    result = validator.validate_diagnostics(code)
    assert result is expected #None is None

    codes = ['iso',32.13,'V4282']
    expected = [False, False, True]
    result = validator.validate_diagnostics(codes)
    assert result == expected

    codes = pd.Series(['iso',32.13,'V4282'])
    expected = pd.Series([False, False, True],index=codes.index)
    result = validator.validate_diagnostics(codes)
    assert result.equals(expected)

    codes = np.array(['iso',32.13,'V4282'])
    expected = np.array([False, False, True])
    result = validator.validate_diagnostics(codes)
    assert np.array_equal(result,expected)


def test_icd9_validator_validate_procedures():
    from icdmappings.validators import ICD9Validator
    validator = ICD9Validator()

    code = 3
    try:
        result = validator.validate_procedures(code)
    except TypeError as e:
        pass

    code = 'abc'
    expected = False
    result = validator.validate_procedures(code)
    assert result == expected

    code = '9957'
    expected = True
    result = validator.validate_procedures(code)
    assert result == expected

    code = None
    expected = None
    result = validator.validate_procedures(code)
    assert result is expected #None is None

    codes = ['iso',32.13,'437']
    expected = [False, False, True]
    result = validator.validate_procedures(codes)
    assert result == expected

    codes = np.array(['iso',32.13,'437'])
    expected = np.array([False, False, True])
    result = validator.validate_procedures(codes)
    assert np.array_equal(result,expected)

    codes = pd.Series(['iso',32.13,'437'])
    expected = pd.Series([False, False, True],index=codes.index)
    result = validator.validate_procedures(codes)
    assert result.equals(expected)
