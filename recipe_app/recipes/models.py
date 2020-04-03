from django.db import models
from recipe_app.users.models import User
from recipe_app.settings import Common


class Ingredient(models.Model):
    name = models.CharField(max_length=50)

    def get_used_recipes(self):
        return self.recipe_set.all()

    def __str__(self):
        return self.name


class Recipe(models.Model):
    DIFFICULTY_LEVELS = (
        ("easy", "Easy"),
        ("medium", "Medium"),
        ("hard", "Hard"),
    )
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to=Common.STATIC_URL + 'img/uploads/')
    description = models.TextField()
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_LEVELS)
    ingredients = models.ManyToManyField(Ingredient)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.PROTECT)
    like = models.IntegerField(default=0)
    vote = models.IntegerField(default=0)
    total_rate = models.IntegerField(default=0)

    class Meta:
        ordering = ['-created_at']

    def get_ingredients(self):
        return ", ".join([str(i) for i in self.ingredients.all()])

    def get_rate(self):
        return 0 if self.vote == 0 else int(self.total_rate / self.vote)

    def liked(self):
        self.like += 1
        self.save()
        return self.like

    def rated(self, rate):
        self.total_rate += rate
        self.vote += 1
        self.save()
        return self.get_rate()

    def __str__(self):
        return self.name

