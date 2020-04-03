from django.contrib import admin
from .models import Recipe, Ingredient


class RecipeAdmin(admin.ModelAdmin):
    ordering = ['-created_at']
    list_display = ['name', 'image', 'difficulty', 'get_ingredients',
                    'owner', 'created_at', 'like', 'vote', 'get_rate']
    search_fields = ['name', 'ingredients__name', 'description', 'owner__username', 'created_at', 'difficulty', ]


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient)
