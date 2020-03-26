# -*- coding:utf-8 -*-

from django.forms import RadioSelect


class ColorSelect(RadioSelect):
    template_name = 'widgets/color_radio/radio.html'
    option_template_name = 'widgets/color_radio/radio_option.html'

