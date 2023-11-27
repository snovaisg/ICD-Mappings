def test_validator_import():
    from icdmappings import Validator
    return

def test_validator_init():
    from icdmappings import Validator
    validator = Validator()
    return

def test_validator():
    from icdmappings import Validator
    validator = Validator()

    validator.show_validators()

    # test icd9 validator

    icd9_dx_a = '5679'
    expected_a = True

    icd9_dx_b = '23'
    expected_b = False

    icd9_dx_c = 5679
    expected_c = False # Must be string

    assert expected_a == validator.validate(icd9_dx_a, expects='icd9_diagnostic')
    assert expected_b == validator.validate(icd9_dx_b, expects='icd9_diagnostic')
    assert expected_c == validator.validate(icd9_dx_c, expects='icd9_diagnostic')
    assert [expected_a, expected_b, expected_c] == validator.validate([icd9_dx_a, icd9_dx_b, icd9_dx_c], expects='icd9_diagnostic')

    icd9_proc_a = '3591'
    expected_a = True

    icd9_proc_b = '12'
    expected_b = False

    icd9_proc_c = 5679
    expected_c = False # Must be string

    assert expected_a == validator.validate(icd9_proc_a, expects='icd9_procedure')
    assert expected_b == validator.validate(icd9_proc_b, expects='icd9_procedure')
    assert expected_c == validator.validate(icd9_proc_c, expects='icd9_procedure')
    assert [expected_a, expected_b, expected_c] == validator.validate([icd9_proc_a, icd9_proc_b, icd9_proc_c], expects='icd9_procedure')
        

