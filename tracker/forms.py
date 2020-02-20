from django import forms


class ProductSearch(forms.Form):
    product_url = forms.CharField(help_text="", label="", widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': "eklemek istediğiniz ürünün adresini yapıştırın",
            'style':'width:500px;'

        }
    ))


class AddProduct(forms.Form):
    def __init__(self, *args, **kwargs):
        super(AddProduct, self).__init__(*args, **kwargs)
        self.fields['alarm_price'].error_messages = {
            'required': '(Alarm fiyatınız sadece rakamlardan oluşmalıdır.)'}

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
