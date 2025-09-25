# from django.db.models.signals import post_save, post_delete
# from django.dispatch import receiver
# from .models import *
# from django.conf import settings
# import requests
# from django.core.mail import send_mail
# from django.conf import settings
#
#
# @receiver(post_save, sender=New)
# def news_signal(sender, instance, created, **kwargs):
#     """
#     :param sender:
#     :param instance:
#     :param created:
#     :param kwargs:
#     :return:
#     Bu funksiya bizda yangilik qo'shilganida barchaga email va telegram orqali xabar yuborish imkonin beradi
#
#     """
#     if created:
#         # message yaratish
#         message = f"Saytda Yangi Xabar\n" \
#                   f"Title: {instance.title}\n" \
#                   f"Qisqacha: {instance.short_desc}\n" \
#                   f"Sana: {instance.create.strftime('%D')}\n"
#
#         email_royxat = [
#             "abddev09@gmail.com",
#             "karimovubaydullox2010@gmail.com",
#             "mrs.anvarova@gmail.com",
#             "nocommentsuu@gmail.com",
#             "mirfotihovakhadicha@gmail.com",
#             "pesuchunk@gmail.com",
#             "dilyormurodqulov417@gmail.com"
#         ]
#         send_mail(
#             subject="Saytda Yangi Xabar Qo'shildi",
#             message=message,
#             from_email=settings.EMAIL_HOST_USER,
#             recipient_list=email_royxat
#         )
#         print("\n\n", "Barchaning emailiga Xabar yuborildi", "\n\n")
#
#         tg_id = [
#             6290800952,
#             7031350814,
#             6651180308,
#             5449575537,
#             6717501063,
#             670626448,
#             727652365,
#         ]
#         for i in tg_id:
#             url = f"https://api.telegram.org/bot{settings.TG_TOKEN}/sendMessage?chat_id={i}&text={message}"
#             requests.get(url)
#
#         message = "Hammaga Xabar yuborib bo'lindi"
#         url = f"https://api.telegram.org/bot{settings.TG_TOKEN}/sendMessage?chat_id={727652365}&text={message}"
#         requests.get(url)











# @receiver(post_save)  # sender=None -> bu universal signal
# def create_signal(sender, instance=None, created=None, *args, **kwargs):
#     print("\nBu Universan signal", sender)
#     print("\nObjects", instance)
#     print("\nYaraldimi", created)
#     print("\n", args, kwargs, "\n\n")
#
#
# @receiver(post_delete, sender=None)
# def delete_signal(sender, instance=None, *args, **kwargs):
#
#     print("\nYangi Signall\nYuboruvchi", sender)
#     print("\nObjects", instance)
#     print("\n", args, kwargs, "\n\n")


@receiver(post_save, sender=Comment)  # sender=Model -> faqat shu model uchun ishlaydi
def comment_signal(sender, instance, created, **kwargs):
    if created:
        message = f"Saytda Yangi Izoh qo'shildi\n" \
                  f"Yangilik: <b>{instance.new.title}</b>\n" \
                  f"User: <b>{instance.user}</b>\n" \
                  f"Message: <b>{instance.message}</b>\n" \
                  f"Sana: <b>{instance.post.strftime('%H:%M / %d-%B %Y')}</b>"
        url = f"https://api.telegram.org/bot{settings.TG_TOKEN}/sendMessage?chat_id={727652365}&text={message}&parse_mode=HTML"
        requests.get(url)


# @receiver(post_delete, sender=Comment)
# def comment_delete_signal(sender, instance, **kwargs):
#     print("Keldi")
#     message = f"Saytdan Comment ochirildi\n Comment: <b>{instance}</b>\n" \
#
#     url = f"https://api.telegram.org/bot{settings.TG_TOKEN}/sendMessage?chat_id={727652365}&text={message}&parse_mode=HTML"
#     a = requests.get(url).text
#     print("ishlayabdi", f"\n\n\n{ a }\n\n\n")




