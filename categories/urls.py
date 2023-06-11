from django.urls import path

from categories.views import CategoryListCreateAPIView, CategoryDetail

app_name = 'categories'
urlpatterns = [
    path('', CategoryListCreateAPIView.as_view(), name='category_list_create'),
    path('<int:pk>/', CategoryDetail.as_view(), name='category-detail-put-delete'),
]
