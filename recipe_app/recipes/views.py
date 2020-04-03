from django.shortcuts import render
from django.views import generic
from .models import Recipe, Ingredient
from django.http import HttpResponseRedirect, HttpResponse
from .forms import *
from django.urls import reverse_lazy
from django.db.models import Count, Q
from django.contrib.auth.mixins import LoginRequiredMixin


class RecipeListView(generic.ListView):
    model = Recipe
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        top_ingredients = Ingredient.objects.all().annotate(num_recipe=Count('recipe')).order_by('-num_recipe')[:10]
        context['top_ingredients'] = top_ingredients

        query = self.request.GET.get('q')
        if query:
            context['q'] = query

        ingredient = self.request.GET.get('i')
        if ingredient:
            context['i'] = ingredient

        return context

    def get_queryset(self):
        query = self.request.GET.get('q')
        ingredient = self.request.GET.get('i')
        if query:
            return Recipe.objects.filter(Q(name__icontains=query) | Q(description__icontains=query) |
                                         Q(difficulty__icontains=query) | Q(created_at__icontains=query) |
                                         Q(ingredients__name__icontains=query) |
                                         Q(owner__username__icontains=query)).distinct()
        elif ingredient:
            return Recipe.objects.filter(ingredients__name=ingredient)
        else:
            return Recipe.objects.all()


class RecipeDetailView(generic.DetailView):
    model = Recipe

    def post(self, request, *args, **kwargs):
        if "like" in request.POST:
            self.get_object().liked()
            return HttpResponseRedirect(self.request.path_info)

        if "rate" in request.POST:
            form = RecipeRateForm(request.POST)

            if form.is_valid():
                self.get_object().rated(int(request.POST["rate"]))
                return HttpResponseRedirect(self.request.path_info)


class RecipeCreate(LoginRequiredMixin, generic.CreateView):
    model = Recipe
    fields = ['name', 'image', 'description', 'difficulty', 'ingredients']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(RecipeCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('recipe-detail', kwargs={'pk': self.object.pk})
