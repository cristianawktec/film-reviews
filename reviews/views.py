from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from .models import Review
from .forms import ReviewForm

import requests
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.admin.views.decorators import staff_member_required

# Lista de reviews publicados
def review_list(request):
    reviews = Review.objects.filter(status=Review.Status.PUBLISHED)
    return render(request, "reviews/list.html", {"reviews": reviews})

# Detalhe de um review individual
def review_detail(request, id):
    review = Review.objects.get(id=id)
    return render(request, "reviews/detail.html", {"review": review})

# Página HTML com o botão para gerar review com IA
@login_required
def nova_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            review.author = request.user
            review.published_at = timezone.now()
            review.save()
            return redirect("reviews:review_list")
    else:
        form = ReviewForm()
    return render(request, 'reviews/nova_review.html', {'form': form})

# Página administrativa para listar todas as reviews
@staff_member_required
def gerenciar_reviews(request):
    reviews = Review.objects.all().order_by("-created_at")
    return render(request, "reviews/gerenciar.html", {"reviews": reviews})

# Editar uma review existente
@staff_member_required
def editar_review(request, id):
    review = Review.objects.get(id=id)
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES, instance=review)
        if form.is_valid():
            form.save()
            return redirect('reviews:gerenciar_reviews')
    else:
        form = ReviewForm(instance=review)
    return render(request, 'reviews/nova_review.html', {'form': form})

# Excluir uma review existente
@staff_member_required
def excluir_review(request, id):
    review = Review.objects.get(id=id)
    review.delete()
    return redirect('reviews:gerenciar_reviews')

# Endpoint que gera o texto com IA via OpenRouter
@csrf_exempt
def gerar_review(request):
    title = request.GET.get("title")
    if not title:
        return JsonResponse({"error": "Informe um título."})

    headers = {
        "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {"role": "user", "content": f"Escreva uma crítica sobre o filme '{title}'"}
        ]
    }

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        json=data,
        headers=headers
    )

    if response.status_code == 200:
        body = response.json()["choices"][0]["message"]["content"].strip()
        return JsonResponse({"body": body})
    else:
        return JsonResponse({"error": response.text})
