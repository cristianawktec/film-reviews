from django.contrib import admin
from django.urls import path
from django.http import JsonResponse
from django.template.response import TemplateResponse
from django.utils.html import format_html
from django import forms
from dotenv import load_dotenv
load_dotenv()

import os
from .models import Review

OPENROUTER_API_KEY = os.getenv("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")

class ReviewAdminForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = '__all__'

class ReviewAdmin(admin.ModelAdmin):
    form = ReviewAdminForm
    change_form_template = "admin/reviews/review/change_form.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('admin/', self.admin_site.admin_view(self.generate_review))
        ]
        return custom_urls + super().get_urls()

    def generate_review(self, request):
        title = request.GET.get("title", "")
        if not title:
            return JsonResponse({"error": "Title is required"}, status=400)

        prompt = f"Escreva uma crítica de filme sobre '{title}'"
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=500
            )
            content = response['choices'][0]['message']['content']
            return JsonResponse({"body": content})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)




