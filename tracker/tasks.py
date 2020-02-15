import time
from celery import shared_task
from .models import Product, MyUser
from tracker.views import crawl_data,make_tiny
from .scripts import telegram


@shared_task
def track_for_discount():
    items = Product.objects.all()
    for item in items:
        if item.status is True:
            data = crawl_data(item.product_url)
            short_url = make_tiny(data["url"])
            if data['last_price'] < float(item.alert_price):
                user_id = item.user_id
                user = MyUser.objects.get(id=user_id)
                telegram.send_message(user.telegram_id,
                                      f'<b>{data["title"].strip()}</b> ürününüz alarm fiyatına düştü.\nSeçili ürün linki:{short_url}')
                selected_item = Product.objects.get(id=item.id)
                selected_item.last_price = data['last_price']
                selected_item.status = False
                if item.product_url.startswith('https://www.amazon.com') :
                    item.store = 'Amazon.tr'
                    item.save()
                elif item.product_url.startswith('https://www.hepsiburada.com'):
                    item.store = 'Hepsiburada'
                    item.save()
                selected_item.save()



while True:
    try :
        track_for_discount()
    except AttributeError :
        print('2 MIN SERVER STOP')
        time.sleep(120)
    time.sleep(60)
