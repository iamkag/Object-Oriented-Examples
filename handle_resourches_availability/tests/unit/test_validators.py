"""
Test the vaidator function
Command line: python -m pytest tests/unit/test_validators.py
"""

import pytest
from app.utils.validators import validate_integer


class TestIntegerValidator:
    def test_valid(self):
        validate_integer('arg',10,0,20,'custom min msg','custom max msg')

    def test_type_error(self):
        with pytest.raises(TypeError) as e:
            validate_integer('arg','10',0,20,'custom min msg','custom max msg')
        assert str(e.value) == 'arg must be an integer'

    def test_min_std_err_msg(self):
        with pytest.raises(ValueError) as ex:
            validate_integer('arg',10, 100)
        assert 'arg' in str(ex.value)
        assert '100' in str(ex.value)
    
    def test_min_custom_err_msg(self):
        with pytest.raises(ValueError) as ex:
            validate_integer('arg',10, 100, custom_min_message='custom min msg')
        assert str(ex.value) == 'custom min msg'
    
    def test_max_std_err_msg(self):
        with pytest.raises(ValueError) as ex:
            validate_integer('arg',10, 1, 5)
        assert 'arg' in str(ex.value)
        assert '5' in str(ex.value)
    
    def test_max_custom_err_msg(self):
        with pytest.raises(ValueError) as ex:
            validate_integer('arg',10, 1, 5, custom_max_message='custom max msg')
        assert str(ex.value) == 'custom max msg'