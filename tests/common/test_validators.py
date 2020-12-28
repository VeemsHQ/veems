import pytest
from django.core.exceptions import ValidationError


from veems.common import validators


class TestValidateLanguage:
    def test_returns_none_if_value_valid(self):
        value = 'en'

        assert validators.validate_language(value=value) is None

    def test_raises_if_value_invalid(self):
        with pytest.raises(ValidationError):
            validators.validate_language(value='zz')
