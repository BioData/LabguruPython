
def validate_required_field(field_value, field_name, action):
    assert field_value, f'{field_name} is required to {action}'


def validate_required_fields(action, **kwargs):
    for item in kwargs.items():
        validate_required_field(item[1], item[0], action=action)


def validate_names(action, **kwargs):
    for item in kwargs.items():
        assert isinstance(item[1], str) and len(item[1]) > 0, f'{item[0]} is required to {action}'

