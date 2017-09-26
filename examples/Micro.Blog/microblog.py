from getpass import getpass
from bessie import BaseClient

import config 


class MicroBlogApi(BaseClient):

	endpoints = config.available_endpoints
	separator = '/'
	base_url='https://micro.blog'

	def __init__(self, path='', path_params=None, token=''):
		self.token = token
		super(self.__class__, self).__init__(path, path_params, token=token)

	# override method from BaseClient to inject Authorization header
	def _prepare_request(self):
		super(self.__class__, self)._prepare_request()
		self.request.headers['Authorization'] = 'Token {}'.format(self.token)


if __name__ == '__main__':
	token = getpass('Token... ')
	mba = MicroBlogApi(token=token)

	# GET - https://micro.blog/posts/all
	posts = mba.posts.all.get()

	print(posts.status_code, posts.reason)
	print(posts.json())
