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


class TestValidateMinimumSize:
    def test_does_not_raise_when_image_meets_requirements(self, mocker):
        mock_image = mocker.Mock(width=10, height=10)
        validator = validators.validate_minimum_size(width=10, height=10)

        validator(image=mock_image)

    def test_raises_if_image_is_too_small(self, mocker):
        mock_image = mocker.Mock(width=9, height=9)
        validator = validators.validate_minimum_size(width=10, height=10)

        with pytest.raises(ValidationError):
            validator(image=mock_image)
