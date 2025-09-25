from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from common.models import Category
from django import forms


class CtgForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'


@login_required(login_url='auth')
def list(request):
    ctgs = Category.objects.all().order_by('-id')

    # paginatsiya yaratish!
    paginator = Paginator(ctgs, per_page=2)
    page = int(request.GET.get('page', 1))
    ctgs = paginator.get_page(page)

    ctx = {
        "position": "list",
        "ctgs": ctgs,
        "paginator": paginator,
        "page": page
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
    return render(request, "dashboard/pages/ctg.html", ctx)


# create | update
def add_ctg(request, pk=None):
    one = None
    if pk:
        one = Category.objects.filter(id=pk).first()
    if request.POST:
        form = CtgForm(request.POST, instance=one)
        if form.is_valid():
            form.save()
            request.session['success'] = "Categoriya Muaffaqiyatli qo'shildi"
        else:
            request.session['error'] = f"Error: {form.errors}"
    return redirect("ctg-list")


# delete
def delete(request, pk):
    try:
        Category.objects.get(id=pk).delete()
        request.session['success'] = 'Categoriya Muaffaqiyatli ochirildi'
    except: ...
    return redirect("ctg-list")





