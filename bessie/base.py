from functools import partial
import requests

try:
	import urlparse as parse
except:
	from urllib import parse


class InvalidApiPathException(Exception):
	pass


class BaseClient(object):
	
	available_paths = []
	separator = '/'
	base_url = ''

	def __init__(self, path='', **kwargs):
		self.path = path
		self.kwargs = kwargs
		self._define_convenience_methods()
		self._prepare_request()
		
	@property
	def full_path(self):
		return parse.urljoin(self.base_url, self.path)
		
	def __getattr__(self, name):
		new_path =self.separator.join((self.path, name)) if self.path else name
		return self.__class__(new_path, **self.kwargs)
		
	def _check_if_valid_path(self, method):
		if self.available_paths and '{} {}'.format(method, self.path) not in self.available_paths:
			raise InvalidApiPathException('{} {} is not a valid path'.format(method, self.path))
			
	def _prepare_request(self):
		self.request = requests.Request()
		
	def _send_request(self, method, **kwargs):
		self._check_if_valid_path(method)
		self.request.url = self.full_path
		self.request.method = method
		self.request.data = kwargs
		return requests.session().send(self.request.prepare())

	def _define_convenience_methods(self):
		actions = ['POST', 'GET', 'PUT', 'PATCH', 'DELETE', 'OPTIONS', 'HEAD']

		for action in actions:
			setattr(self, action.lower(), partial(self._send_request, action))


