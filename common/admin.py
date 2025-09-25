from django.contrib import admin
from .models import Category, New, Comment, Contact, Subscribe


# Register your models here.


# UYga vazifa: anashu fayl cho'tki bo'lsin!!!
# Uyga vazifa2: Barcha classlarga Meta class yozib chiqqish!!

# Bonus Dars -> StackInline!!! ForeinKey olingan tablitsalar uchun ishlaydi!!
class NewsInline(admin.StackedInline):
    model = New
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    inlines = [NewsInline]


admin.site.register(New)
admin.site.register(Comment)
admin.site.register(Contact)
admin.site.register(Subscribe)
