from django.core.validators import MinValueValidator
from django.db import models

from foodgram_backend import model_settings as set
from users.models import User


class Tag(models.Model):
    """Модель тега."""

    name = models.CharField(
        'Название тега',
        max_length=set.TAG_NAME_LENGTH,
        unique=True,
        blank=False,
        null=False,
        db_index=True,
        help_text='Укажите название тега',
    )
    color = models.CharField(
        'Цвет тега',
        max_length=set.TAG_COLOR_NAME_LENGTH,
        blank=False,
        null=False,
        help_text='Добавьте цвет тега в hex формате',
    )
    slug = models.SlugField(
        'Идентификатор тега',
        unique=True,
        blank=False,
        null=False,
        help_text='Добавьте слаг',
    )

    class Meta:
        """Мета настройка отображения модели тега."""
        ordering = ['name']
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        """Строковое отображение модели тега."""

        return self.name


class Ingredient(models.Model):
    """Модель ингридиента."""

    name = models.CharField(
        'Название ингридиента',
        max_length=set.INGREDIENT_NAME_LENGTH,
        null=False,
        blank=False,
        db_index=True,
        help_text='Укажите название ингредиента'
    )
    measurement_unit = models.CharField(
        'Мера измерения ингридиента',
        max_length=set.INGREDIENT_MEASUREMENT_UNIT_LENGTH,
        blank=False,
        null=False,
        help_text='Укажите меру измерения, например граммы или литры',
    )

    class Meta:
        """Мета настройки отображения модели ингредиента и проверка
        уникальности количества ингредиента."""

        ordering = ['name']
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='unique_measurement',
            )
        ]

    def __str__(self):
        """Строковое отображение модели ингредиента."""

        return self.name


class Recipe(models.Model):
    """Модель рецепта."""

    tags = models.ManyToManyField(
        Tag,
        related_name='recipe',
        verbose_name='Теги',
        help_text='Отметьте подходящие теги'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipe',
        verbose_name='Автор рецепта',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredientsAmount',
        related_name='recipe',
        verbose_name='Ингредиенты',
        help_text='Добавьте необходимые ингредиенты',
    )
    name = models.CharField(
        'Название рецепта',
        max_length=set.RECIPE_NAME_LENGTH,
        null=False,
        blank=False,
        help_text='Назовите рецепт',
    )
    image = models.ImageField(
        'Фотография блюда',
        upload_to='meal/images/',
        null=False,
        blank=False,
        help_text='Добавьте изображение готового блюда',
    )
    text = models.TextField(
        'Описание рецепта',
        max_length=set.RECIPE_TEXT_LENGTH,
        null=False,
        blank=False,
        help_text='Опишите процесс приготовления блюда',
    )
    cooking_time = models.IntegerField(
        'Время приготовления (в минутах)',
        null=False,
        blank=False,
        validators=[MinValueValidator(
            1,
            message='Время приготовления должно быть больше 1'
        )
        ],
        help_text='Укажите время приготовления в минутах',
    )
    create_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        """Мета настройки отображения модели рецепта."""

        ordering = ['-create_at']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        """Строковое отображение модели рецепта."""

        return self.name


class RecipeIngredientsAmount(models.Model):
    """Вспомогательная модель для указания количества ингредиента."""

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe',
        verbose_name='Рецепт',
        help_text='Выберите рецепт'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredient',
        verbose_name='Ингредиент',
        help_text='Выберите ингредиент'
    )
    amount = models.IntegerField(
        'Необходимое количество ингредиента.',
        validators=[
            MinValueValidator(
                1,
                message='Нет ингредиентов - нет блюда!'
            )
        ],
        help_text='Сколько ингредиента нужно '
                  'добавить в соответствующей мере изменения?'
    )

    class Meta:
        """Сортировка выдачи и проверка уникальности ингредиентов."""

        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_ingredients',
            )
        ]
        ordering = ['recipe']
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецептах'

    def __str__(self):
        """Строковое отображение ингредиента в рецепте."""

        return (f'Ингрединет: {self.ingredient.name}'
                f'из рецепта: {self.recipe.name}')


class ShoppingCart(models.Model):
    """Модель карты покупок."""

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Рецепт',
        help_text='Выберите рецепт',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Покупатель',
    )
    create_at = models.DateTimeField(
        'Дата добавления в покупки.',
        auto_now_add=True,
    )

    class Meta:
        """Представление модели и валидация уникальности."""

        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'user'],
                name='unique_recipes',
            )
        ]
        ordering = ['-create_at']
        verbose_name = 'Покупка'
        verbose_name_plural = 'Покупки'

    def __str__(self):
        """Строковое отображение модели карты покупок."""

        return f'Рецепт "{self.recipe.name}" в покупках у {self.user}'


class FavoriteRecipe(models.Model):
    """Модель избранных рецептов."""

    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Избранный рецепт',
        help_text='Выберите рецепт',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Автор подписки',
    )
    create_at = models.DateTimeField(
        'Дата добавления в избранное',
        auto_now_add=True
    )

    class Meta:
        """Мета настройки отображения модели избранного и проверка
        уникальности связи рецепта и пользоватля."""

        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'user'],
                name='unique_favorite',
            )
        ]
        ordering = ['-create_at']
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'

    def __str__(self):
        """Строковое отображения избранного."""

        return f'Рецепт "{self.recipe}" в избранном у {self.user}'
