import asyncio
from asyncgcm import GCM

API_KEY = '' # YOUR API KEY

gcm = GCM(API_KEY)

reg_ids = [reg_id1, reg_id2] # etc

data = {'message': 'new message', 'title': 'hello world'}

async def resp(reg_ids, data):
	resp = await gcm.json_message(registration_ids=reg_ids, data=data, time_to_live=1024)
	return resp

loop = asyncio.get_event_loop()
result = loop.run_until_complete(resp(reg_ids, data))
print(resp)
loop.close()
