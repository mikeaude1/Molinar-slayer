from django import forms
from django.contrib.auth.forms import AuthenticationForm
# from captcha.fields import CaptchaField
from hcaptcha_field import hCaptchaField

class CaptchaAuthenticationForm(AuthenticationForm):
    # Replace simple captcha with hCaptcha (image selection)
    hcaptcha = hCaptchaField()