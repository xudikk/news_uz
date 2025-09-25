import random

import requests
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
# Create your views here.
from .models import Category, New, Comment, Contact, Subscribe
from django.db.models import Q

from django.core.mail import send_mail
from django.conf import settings


# pip install SpeechRecognition pyaudio


def index(request):
    news = New.objects.all().order_by('-create')  # queryset
    random_news = [news[random.randint(0, len(news) - 1)], news[random.randint(0, len(news) - 1)]]
    aktual = New.objects.filter(Q(title__icontains="tramp") | Q(short_desc__icontains="tramp"))[:3]

    ctx = {
        "news": news,
        "random_news": random_news,
        "aktual": aktual
    }
    return render(request, 'index.html', ctx)


def ctg(request, slug):
    one_ctg = Category.objects.filter(slug=slug).first()
    if not one_ctg:
        return render(request, 'category.html', {"error": 404})

    news = New.objects.filter(ctg=one_ctg).order_by('-id')
    if not news:
        return render(request, 'category.html', {"error": 404})

    paginator = Paginator(news, 2)
    page = request.GET.get("page", 1)  # 1, 2, 3, 4,
    result = paginator.get_page(page)

    ctx = {
        "one_ctg": one_ctg,
        "news": result,
        "len": len(news),
        "paginator": paginator,
        "page": int(page)
    }
    return render(request, 'category.html', ctx)


def view(request, pk):  # pk=primary_key( id )
    one_new = New.objects.filter(id=pk).first()
    if not one_new:
        return render(request, 'view.html', {"error": 404})
    one_new.views += 1
    one_new.save()

    # comment yozish qismi:
    if request.POST:
        user = request.POST.get('user', None)
        message = request.POST.get('message', None)
        parent_id = request.POST.get('parent_id', 0)  # 3 -> true, 0 -> false
        if None in [user, message]:
            pass
        else:
            Comment.objects.create(
                new=one_new,
                user=user,
                message=message,
                parent_id=None if not parent_id else int(parent_id),
                is_sub=bool(parent_id)
            )
            return redirect("view", pk=pk)

    # random yangilik olish qism
    news = New.objects.filter(ctg=one_new.ctg)
    comments = Comment.objects.filter(is_sub=False, new=one_new).order_by('-post')
    ctx = {
        "one_new": one_new,
        'comments': comments,
        "count": len(comments)
    }

    if len(news) > 2:
        random_news = [news[random.randint(0, len(news) - 1)], news[random.randint(0, len(news) - 1)]]
        ctx["random_news"] = random_news

    return render(request, 'view.html', ctx)


def search(request):
    key = request.GET.get('search', None)
    if not key:
        return render(request, 'search.html', {'error': 404})

    news = New.objects.filter(Q(title__icontains=key) |
                              Q(short_desc__icontains=key) |
                              Q(description__icontains=key) |
                              Q(tags__icontains=key))

    paginator = Paginator(news, 5)
    page = request.GET.get("page", 1)
    result = paginator.get_page(page)

    ctx = {
        "news": result,
        "count": paginator.count,
        "paginator": paginator,
        "page": page,
        "key": key,
    }
    return render(request, 'search.html', ctx)


def cnt(request):
    if request.POST:
        try:
            contact = Contact.objects.create(
                ism=request.POST['ism'],
                phone=request.POST['phone'],
                xabar=request.POST['xabar'],
            )
            request.session['success'] = "Murojaatingiz uchun Raxmat xabaringiz adminlarga yuborildi"

            message = f"Saytdan Yangi Kontakt\n" \
                      f"Ism: {contact.ism}\n" \
                      f"Telefon Raqam: {contact.phone}\n\n" \
                      f"Xabar: {contact.xabar}"

            url = f"https://api.telegram.org/bot{settings.TG_TOKEN}/sendMessage?chat_id={727652365}&text={message}"
            requests.get(url)


        except:
            ...  # pass == ...

        return redirect("contact")

    success = request.session.get('success', None)
    try:
        del request.session['success']
    except:
        ...

    ctx = {
        "success": success or ""
    }
    return render(request, 'contact.html', ctx)


def add_to_subs(request, path):
    if request.POST:
        try:
            Subscribe.objects.create(
                email=request.POST['email']
            )
        except:
            pass

    return redirect(path)
