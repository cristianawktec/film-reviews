from django.urls import path
from . import views

app_name = "reviews"

urlpatterns = [
    path("", views.review_list, name="review_list"),
    path("<int:id>/", views.review_detail, name="review_detail"),
    path('base/', views.review_base, name='review_base'),
]
