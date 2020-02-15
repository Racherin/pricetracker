from __future__ import with_statement

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from .models import Product, MyUser
import random
from tracker import forms
from bs4 import BeautifulSoup
import requests
from django.template.loader import render_to_string
from .scripts import telegram
import string
from django.contrib import messages

import contextlib

try:
    from urllib.parse import urlencode

except ImportError:
    from urllib import urlencode
try:
    from urllib.request import urlopen

except ImportError:
    pass
import sys


def make_tiny(url):
    request_url = ('http://tinyurl.com/api-create.php?' + urlencode({'url': url}))
    with contextlib.closing(urlopen(request_url)) as response:
        return response.read().decode('utf-8 ')


def crawl_data(url):
    # User Agent is to prevent 403 Forbidden Error
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36 Edg/80.0.361.48'}
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.text, "html.parser")
    if url.startswith('https://www.amazon.com.tr/'):
        product_title = str(soup.find(id="productTitle").text).strip()
        print('Kontrol edilen ürün :' + product_title)
        product_price = soup.find(id="priceblock_ourprice").text.strip()
        img = soup.find(id='landingImage')
        product_image = img['src']
        clean_price = float(product_price.strip('₺').replace(',', '.'))
        url = url
        return {'title': str(product_title).strip(), 'last_price': clean_price, 'product_image': product_image,
                'price': product_price,
                'url': url}
    elif url.startswith('https://www.hepsiburada.com/'):
        product_title = soup.find(id="product-name").text.strip()
        print('Kontrol edilen ürün :' + product_title)
        product_price = soup.find(id='offering-price').text.strip().strip(' ( / adet)')
        img = soup.select_one('.product-image')
        product_image = img['data-img'].replace('#imgSize', '479')
        clean_price = float(product_price[:8].replace('TL', '').replace('.', '').replace(',', '.'))
        url = url
        return {'title': str(product_title).strip(), 'last_price': clean_price, 'product_image': product_image,
                'price': product_price,
                'url': url}


def index(request):
    global title, price, image, price_int, url
    product_url_form = forms.ProductSearch(request.POST or None)
    product_add_form = forms.AddProduct(request.POST or None)

    randomnumber = random.randint(1, 3)
    if randomnumber == 1:
        context = {
            'title': 'Logitech S150 1+1 USB Speaker',
            'price': '₺103,89',
            'image': "https://images-na.ssl-images-amazon.com/images/I/81tLaar-pFL._AC_SX679_.jpg",
            'form': product_url_form,
            'form_add': product_add_form,
            'price_converted': 103.89,
            'url': 'https://www.amazon.com.tr/dp/B000XUQ2LI/ref=s9_acsd_top_hd_bw_bExpRGp_c2_x_1_t?pf_rd_m'
                   '=A1UNQM1SR2CHM&pf_rd_s=merchandised-search-11&pf_rd_r=6Q73A0AFSCNW88H1EWM5&pf_rd_t=101&pf_rd_p'
                   '=b1b6f5bb-5ce7-58c0-9232-65c7307ffd5d&pf_rd_i=13709923031',
        }
    elif randomnumber == 2:
        context = {
            'title': 'Hasbro Monopoly Dijital Bankacılık',
            'price': '₺138,50',
            'image': "https://images-na.ssl-images-amazon.com/images/I/71hiHsg%2BjpL._SL1000_.jpg",
            'form': product_url_form,
            'form_add': product_add_form,
            'price_converted': 138.50,
            'url': 'https://www.amazon.com.tr/dp/B07C2B7K7S/ref=br_msw_pdt-6?_encoding=UTF8&smid=A1UNQM1SR2CHM'
                   '&pf_rd_m=A1UNQM1SR2CHM&pf_rd_s=&pf_rd_r=80JWJR2121CSH122TX51&pf_rd_t=36701&pf_rd_p=2b662ac9-8b96'
                   '-4a83-a7be-283154520a63&pf_rd_i=desktop',
        }
    elif randomnumber == 3:
        context = {
            'title': 'Apple iPhone 11 Akıllı Telefon, 64 GB',
            'price': '₺7.349,00',
            'image': "https://images-na.ssl-images-amazon.com/images/I/712FrYrG05L._SL1500_.jpg",
            'form': product_url_form,
            'form_add': product_add_form,
            'price_converted': 7349.00,
            'url': 'https://www.amazon.com.tr/Apple-iPhone-Ak%C4%B1ll%C4%B1-Telefon-Beyaz/dp/B07XZPYV1T/ref'
                   '=zg_bs_electronics_home_2?_encoding=UTF8&psc=1&refRID=RV5YT87S0KEDRKVK4T16',
        }

    if product_url_form.is_valid():
        product_url = product_url_form.cleaned_data.get('product_url')

        try:
            product_data = crawl_data(product_url)
            if not product_data['url'].startswith('https://'):
                messages.error(request, 'Yanlış url.')
                redirect('index')
            title = product_data['title']
            price = product_data['price']
            image = product_data['product_image']
            price_int = product_data['last_price']
            url = product_data['url']
            context = {
                'title': title,
                'price': price,
                'image': image,
                'form': product_url_form,
                'form_add': product_add_form,
                'price_converted': price_int,
                'url': url,

            }
            return render(request, 'index.html', context)
        except AttributeError:
            messages.warning(request, 'Ürün bulunamadı. <a href="/" style="color:#AA3333">Hata Bildir</a>')
            redirect('index')

    if product_add_form.is_valid():
        alert_price = product_add_form.cleaned_data.get('alarm_price')
        new_product = Product()
        new_product.user = request.user
        new_product.title = title
        new_product.status = True
        new_product.store = 'Amazon'
        new_product.alert_price = alert_price
        new_product.last_price = price_int
        new_product.product_url = url
        new_product.alert = False
        new_product.save()
        return redirect('manage')

    return render(request, 'index.html', context)


def logoutUser(request):
    logout(request)
    return redirect('index')


def manage(request):
    products = Product.objects.filter(user=request.user)
    html = render_to_string("telegram.html", {"telegram_id": MyUser.telegram_id})
    return render(request, 'manage.html', {'products': products})


def active_notification(request, id):
    product = get_object_or_404(Product, id=id)
    product.status = True
    product.save()
    return redirect('manage')


def disable_notification(request, id):
    product = get_object_or_404(Product, id=id)
    product.status = False
    product.save()
    return redirect('manage')


def delete_product(request, id):
    product = get_object_or_404(Product, id=id)
    product.delete()
    return redirect('manage')


def install_telegram(request):
    user = MyUser.objects.get(username=request.user.get_username())
    telegram_chat_id_submit_form = forms.ChatIdSubmit(request.POST or None)
    if telegram_chat_id_submit_form.is_valid():
        chat_id = telegram_chat_id_submit_form.cleaned_data.get('chat_id')
        if len(chat_id) == 9 and chat_id.isnumeric():
            user.telegram_id = chat_id
            messages.info(request, 'Chat ID tanımlama başarılı.')
            user.telegram_status = True
            user.save()
        else:
            messages.info(request, 'Chat ID tanımlama başarısız, lütfen girdiğiniz değerleri kontrol ediniz.')

    return render(request, 'telegram.html', context={'form': telegram_chat_id_submit_form})


def telegram_code_request(request):
    user = MyUser.objects.get(username=request.user.get_username())
    return redirect('telegram')
