from veems.common.templatetags import to_json


def test_to_json():
    result = to_json.to_json(data={'hello': 'world'}, indent=None)

    assert result == '{"hello": "world"}'
