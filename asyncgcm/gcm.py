import asyncio
from aiohttp import ClientSession
import json


GCM_URL = 'https://gcm-http.googleapis.com/gcm/send'


class GCMException(Exception):
	pass

class GCMMissingRegistrationTokenException(GCMException):
	pass

class GCMInvalidRegistrationTokenException(GCMException):
	pass

class GCMUnregisteredDeviceException(GCMException):
	pass

class GCMInvalidPackageName(GCMException):
	pass

class GCMAuthenticationException(GCMException):
	pass

class MismatchedSenderException(GCMException):
	pass

class GCMInvalidJSONException(GCMException):
	pass

class GCMMessageTooBigException(GCMException):
	pass

class GCMInvalidDataKeyException(GCMException):
	pass

class GCMInvalidTTLException(GCMException):
	pass

class GCMTimeoutException(GCMException):
	pass

class GCMUnavailableException(GCMException):
	pass

class DeviceMessageRateExceededException(GCMException):
	pass



class ValidationDecorator:
	"""
	Validation Decorator
	"""

	# 4 weeks in seconds
	TTL = 7 * 24 * 60 * 60 * 4

	def __init__(self, func):
		"""
		take a function
		"""

		self.func = func
	
	def _validate_time_to_live(self, val):
		if not (0 < val < self.TTL):
			raise GCMInvalidTTLException("Invalid TTL value")

	def _validate_registration_ids(self, reg_ids):
		if len(reg_ids) > 1000:
			raise ValueError("reg ids cannot be greater than 1000")

	def _validate(self, **kwargs):
		for k,v in kwargs.items():
			validate_method = getattr(self, '_validate_{}'.format(k), None)
			if validate_method:
				validate_method(v)

	def __call__(self, **kwargs):
		self._validate(**kwargs)
		return self.func(**kwargs)
		

class GCM:

	def __init__(self, api_key, url=GCM_URL, proxy=None, timeout=None):
		"""
		api_key: google api key
		url: url of GCM service
		proxy: aiohttp.ProxyConnector see aiohttp documentation
		timeout: TODO
		"""	

		self.api_key = api_key
		self.url = url
		self.proxy = proxy
		self.timeout = timeout
		self._headers = {'Authorization': 'key='+self.api_key}

	async def plaintext_message(self, **kwargs):
		"""
		makes plaintext request
		"""

		if 'registration_id' not in kwargs:
			raise GCMMissingRegistrationTokenException("Missing registration_id")

		payload = self._prepare_payload(**kwargs)
		data = payload.pop('data')
		for k,v in data.items():
			payload['data.{}'.format(k)] = v

		await self._request(payload)

	async def topic_message(self):
		"""
		TODO
		"""
		pass

	async def json_message(self, **kwargs):
		"""
		makes json request
		"""

		payload = self._prepare_payload(**kwargs)
		await self._request(json.dumps(kwargs))

	@ValidationDecorator
	def _prepare_payload(**kwargs):
		"""
		validate some fields
		"""

		if 'registration_id' in kwargs:
			return kwargs
		if ('to' in kwargs) and ('registration_ids' in kwargs):
			raise ValueError("to and reg_ids")
			
		if ('to' not in kwargs) and ('registration_ids' not in kwargs):
			raise GCMMissingRegistrationTokenException("Missing registration_ids")

		return kwargs
		
	async def _request(self, data):
		"""
		make request to gcm
		"""

		headers = {}
		if isinstance(data, str):
			headers['Content-Type'] = 'application/json'

		async with ClientSession(headers=self._headers, connector=self.proxy) as session:
			try:
				async with session.post(self.url, data=data, headers=headers) as resp:
					resp = await resp.text()


					if resp.status == 400:
						raise GCMInvalidJSONException("Malformed JSON request")

					if resp.status == 401:
						raise GCMAuthenticationException("Error authorization account")

					if resp.status == 500:
						raise GCMUnavailableException("Service Unavailable")

					else:
						raise GCMException(resp)

					return resp

			except:
				raise GCMException(resp)

			finally:
				session.close()

