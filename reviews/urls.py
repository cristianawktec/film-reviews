from django.urls import path
from . import views

app_name = "reviews"

urlpatterns = [
    path("", views.review_list, name="review_list"),
    path("<int:id>/", views.review_detail, name="review_detail"),
    path("nova_review/", views.nova_review, name="nova_review"),
    path("gerar_review/", views.gerar_review, name="gerar_review"),
    path("gerenciar/", views.gerenciar_reviews, name="gerenciar_reviews"),
    path("editar/<int:id>/", views.editar_review, name="editar_review"),
    path("excluir/<int:id>/", views.excluir_review, name="excluir_review"),

]
