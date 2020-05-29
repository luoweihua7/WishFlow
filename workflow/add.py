#!/usr/bin/python
#_*_ coding:UTF-8 _*_
#
# Copyright by Larify. All Rights Reserved.

import json
import urllib
import urllib2
import sys
import re

from workflow import Workflow3
from airtable import Airtable
from i18n import lang

reload(sys)
sys.setdefaultencoding('utf-8')

def get_app_id(url = ''):
	search = re.search(r'(http|https)\:\/\/(itunes|apps).apple.com\/(\w+\/)?app\/([^\/]*)\/id(\d+)\?', url)
	if search:
		app_id = search.group(5)
		return app_id
	else:
		return ""

def search(id_list = []):
	url = 'https://itunes.apple.com/lookup?id=%s' % ','.join(id_list)
	opener = urllib2.build_opener(urllib2.HTTPHandler)
	request = urllib2.Request(url)
	url = opener.open(request)
	result = url.read()
	store_data = json.loads(result)
	return store_data['results']

def list_wishlist():
	data = table.list_records()
	records = data['records']
	id_list = []
	for item in records:
		fields = item['fields']
		if fields:
			id_list.append(get_app_id(fields['URL']))
	
	store_items = search(id_list)
	items = [{
		"title": item['trackName'],
		"subtitle": '  '.join(
				[lang['APP_PRICE'] + item['formattedPrice'], 
				lang['APP_VERSION'] + item['version'], 
				lang['APP_RATE'] + item['trackContentRating']
			]),
		"arg": item['trackViewUrl'],
		"icon": DEFAULT_ICON
	} for item in store_items]
	return items

def main(wf):
	arg_len = len(wf.args)
	if arg_len >= 4:
		is_add = wf.args[3] == 'add'
		if is_add and arg_len == 4:
			wf.add_item(title = lang['ADD_TITLE_TIP'], subtitle = lang['ADD_SUBTITLE_TIP'], icon = DEFAULT_ICON, valid = True)
			wf.send_feedback()
			return
		elif is_add and arg_len == 5:
			url = wf.args[4]
			app_id = get_app_id(url)
			if len(app_id) == 0:
				wf.add_item(title = lang['ERR_URL_TITLE'], subtitle = lang['ERR_URL_SUBTITLE'], icon = DEFAULT_ICON, valid = True)
			else:
				store_items = search(id_list = [app_id])
				for item in store_items:
					trackName = item['trackName']
					trackViewUrl = item['trackViewUrl']
					trackId = item['trackId']
					formattedPrice = item['formattedPrice']
					trackContentRating = item['trackContentRating']
					version = item['version']

					wf.add_item(
						title = trackName,
						subtitle = '  '.join([lang['APP_PRICE']+formattedPrice, lang['APP_VERSION']+version, lang['APP_RATE']+trackContentRating]),
						arg = '--add %s' % trackId,
						icon = DEFAULT_ICON,
						valid = True
					)
			wf.send_feedback()
			return
	
	items = list_wishlist()
	for item in items:
		wf.add_item(title = item['title'], subtitle = item['subtitle'], arg = item['arg'], icon = item['icon'])
	wf.send_feedback()

if __name__ == '__main__':
	wf = Workflow3()
	api_key = wf.args[0]
	db = wf.args[1]
	tb = wf.args[2]
	DEFAULT_ICON = 'icon.png'
	table = Airtable(api_key, db, tb)

	sys.exit(wf.run(main))