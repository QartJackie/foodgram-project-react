from rest_framework.serializers import ValidationError


def unique_user_subscribe_validate(self, data):
    """Валидатор подписок, запрещает подписку на самого себя"""

    user = self.context.get('request').user
    if user == data['author']:
        raise ValidationError(
            'Подписка на самого себя невозможна.'
        )
    return data
