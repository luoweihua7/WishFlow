# -*- coding: utf-8 -*-

import os

_dics = {
  'en_US': {
    'TITLE_DEFAULT' : u'Get Exchange Rate Failure',
    'SUBTITLE_DEFAULT' : u'Please try again...',
  },
  'zh_CN': {
    'TITLE_DEFAULT' : u'汇率转换失败',
    'SUBTITLE_DEFAULT' : u'请重试，或换一个汇率试试...',
    'ERR_PARAMS_TITLE' : u'参数配置错误',
    'ERR_PARAMS_SUBTITLE' : u'请先修改参数后再试...',
    'ERR_URL_TITLE' : u'链接错误',
    'ERR_URL_SUBTITLE' : u'无法从链接中分析出AppID...',
    'ADD_TITLE_TIP' : u'添加到愿望清单',
    'ADD_SUBTITLE_TIP' : u'请输入App链接...',
    'APP_PRICE' : u'价格：',
    'APP_VERSION' : u'版本：',
    'APP_RATE' : u'评分：',
  }
}

local = os.popen('defaults read -g AppleLocale').read().rstrip()

try:
  lang = _dics[local]
  lang = _dics['zh_CN']
except KeyError as e:
  lang = _dics['zh_CN']


  