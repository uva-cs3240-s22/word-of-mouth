from django import template
register = template.Library()


def filter_favorite(self, user):
    return self.filter(favorites=user)

register.filter('filter_favorite', filter_favorite)