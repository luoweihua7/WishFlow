import json
import urllib
import urllib2
import json
import posixpath

class Airtable(object):
	def __init__(self, api_key, db_name, table_name ):
		self.base_url = 'https://api.airtable.com/v0/%s/%s' % (db_name, table_name)
		self.headers = {'Authorization': 'Bearer %s' % api_key}

	def __request(self, url, data = None, method = "GET"):
		opener = urllib2.build_opener(urllib2.HTTPHandler)
		request = urllib2.Request(url, data, self.headers)
		if method == "DELETE":
			request.get_method = lambda: method
		elif method == "POST":
			request.get_method = lambda: method
		url = opener.open(request)
		result = url.read()
		return json.loads(result)

	def list_records(self):
		return self.__request(self.base_url)

	def create_record(self, name, url, price = 0):
		return self.__request(self.base_url)
	
	def delete_record(self, id):
		url = posixpath.join(self.base_url, id)
		return self.__request(url, None, "DELETE")