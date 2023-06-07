from django.urls import path

from categories.views import CategoryListCreateAPIView

app_name = 'categories'
urlpatterns = [
    path('', CategoryListCreateAPIView.as_view(), name='category_list_create')
]
