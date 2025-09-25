
# Bu yerda biz Global ctx larni yozamiz!!
from common.models import Category, New


def valyuta():
    # url = 'https://cbu.uz/uz/arkhiv-kursov-valyut/json/'
    # response = rq.get(url).json()
    response = [
        {
            "Ccy": "USD",
            "Rate": "12514.34",
            "Diff": "-67.39",
        },
        {
            "Ccy": "RUB",
            "Rate": "156.41",
            "Diff": "0",
        },
        {
            "Ccy": "EUR",
            "Rate": "14600.48",
            "Diff": "67.39",
        },
    ]
    return response


def main(request):
    ctgs = Category.objects.filter(is_menu=True)
    svejiy_news = New.objects.all().order_by('-id')

    return {
        "valyuta": valyuta(),
        "ctgs": ctgs,
        "svejiy_news": svejiy_news
    }




