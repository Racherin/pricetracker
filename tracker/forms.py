from django import forms


class ProductSearch(forms.Form):
    product_url = forms.CharField(help_text="", label="", widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'value': "https://www.amazon.com.tr/dp/B07ZVX137Q/ref=br_msw_pdt-4/262-3157668-0814319?_encoding=UTF8&smid=ACDRSC09YA6CQ&pf_rd_m=A1UNQM1SR2CHM&pf_rd_s=&pf_rd_r=0KAXS1QT6PSRYTVE2KD8&pf_rd_t=36701&pf_rd_p=0797917a-6b14-4146-a3c5-b3503fa4cb03&pf_rd_i=desktop",
            'placeholder': "eklemek istediğiniz ürünün adresini yapıştırın",

        }
    ))


class AddProduct(forms.Form):
    def __init__(self, *args, **kwargs):
        super(AddProduct, self).__init__(*args, **kwargs)
        self.fields['alarm_price'].error_messages = {
            'required': 'Alarm Fiyatı :'}

    alarm_price = forms.CharField(help_text="", label="", widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'alarm fiyatı giriniz'

        }
    ))


class ChatIdSubmit(forms.Form):
    chat_id = forms.CharField(help_text="Chat ID numaranız sadece 9 rakamdan oluşan bir sayıdır", label="", widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': "Size ait Chat ID numaranızı giriniz.",
        }
    ))
