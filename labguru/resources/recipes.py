# labguru/resources/recipes.py
from labguru.exceptions import LabguruError
from labguru.resources.base import BaseResource


class RecipesResource(BaseResource):
    """Recipes: delete only (the only documented endpoint)."""

    resource_name = "recipes"

    def list(self, *args, **kwargs):
        raise LabguruError("recipes supports delete only; list is not available")

    def get(self, *args, **kwargs):
        raise LabguruError("recipes supports delete only; get is not available")

    def create(self, *args, **kwargs):
        raise LabguruError("recipes supports delete only; create is not available")

    def update(self, *args, **kwargs):
        raise LabguruError("recipes supports delete only; update is not available")
