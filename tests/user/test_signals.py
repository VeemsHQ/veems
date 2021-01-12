import pytest

from veems.user import signals

MODULE = 'veems.user.signals'
pytestmark = pytest.mark.django_db


def test_login_on_activation(mocker):
    mock_login = mocker.patch(f'{MODULE}.login')
    mock_request = mocker.Mock()
    mock_user = mocker.Mock()

    signals.login_on_activation(
        sender=mocker.Mock(),
        user=mock_user,
        request=mock_request,
    )

    assert mock_login.called
    mock_login.assert_called_once_with(
        mock_request,
        mock_user,
    )
