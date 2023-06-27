from rest_framework.serializers import ValidationError


def unique_user_subscribe_validate(self, data):
    """Валидатор подписок, запрещает подписку на самого себя"""

    if self.context.get('request').user == data['author']:
        raise ValidationError(
            'Подписка на самого себя невозможна.'
        )
    return data
