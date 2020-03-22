# -*- coding:utf-8 -*-
from django.shortcuts import render

from web.forms.account import RegisterModelForm


def register(request):
    form = RegisterModelForm()
    return render(request, 'register.html', {'form': form})