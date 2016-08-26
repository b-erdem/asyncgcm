import asyncio
from asyncgcm import GCM

API_KEY = '' # YOUR API KEY

gcm = GCM(API_KEY)

reg_id = '' # registration_id

data = {'message': 'new message', 'title': 'hello world'}


async def resp(reg_id, data):
	resp = await gcm.plaintext_message(registration_id=reg_id,
	 data=data,
	 time_to_live=1024)
	return resp

loop = asyncio.get_event_loop()
result = loop.run_until_complete(resp(reg_id, data))
print(resp)
loop.close()
