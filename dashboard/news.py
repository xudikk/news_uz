from django.core.paginator import Paginator

from common.models import New
from django import forms
from django.shortcuts import render, redirect


class NewForm(forms.ModelForm):
    class Meta:
        model = New
        fields = '__all__'


def list_or_one(request, pk=None):
    print(pk)
    if pk:
        new = New.objects.filter(id=pk).first()
        if not new:
            request.session['error'] = "Ushbu Yangilik topilmadi"
            return redirect("news-list")
        ctx = {
            "new": new,
            "position": "detail"
        }
    else:
        news = New.objects.all().order_by('-id')

        # paginatsiya
        paginator = Paginator(news, per_page=20)
        page = request.GET.get("page", 1)
        result = paginator.get_page(page)

        ctx = {
            "news": result,
            "paginator": paginator,
            'page': int(page),
            "position": "list"
        }

    success = request.session.get('success')
    error = request.session.get('error')
    ctx['success'] = success
    ctx['error'] = error
    try:
        del request.session['success']
    except:
        ...
    try:
        del request.session['error']
    except:
        ...

    return render(request, "dashboard/pages/news.html", ctx)




def add_edit(request, pk=None):
    obj = None
    if pk:
        obj = New.objects.filter(id=pk).first()

    form = NewForm(instance=obj)
    if request.POST:
        form = NewForm(request.POST, request.FILES or None, instance=obj)
        if form.is_valid():
            form.save()
            request.session['success'] = 'Yangilik Muaffaqiyatli qo\'shildi'
        else:
            request.session['error'] = f"Error: {form.errors}"
        return redirect("news-list")
    ctx = {
        "form": form,
        "position": "form",
        "obj": obj
    }
    return render(request, "dashboard/pages/news.html", ctx)


def delete(request, pk):
    try:
        New.objects.get(id=pk).delete()
        request.session['success'] = 'Yangilik Muaffaqiyatli ochirildi'
    except: ...
    return redirect("news-list")










