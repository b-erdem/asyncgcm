# asyncgcm
Python async client for Google Cloud Messaging (GCM)

### Usage

```python
import asyncio
from asyncgcm import GCM

API_KEY = "YOUR API KEY"

gcm = GCM(API_KEY)

message = {'message': 'new message', 'title': 'app title'}

reg_ids = [reg_id1, reg_id2] # list of reg ids


async def response(reg_ids, data):
  resp = await gcm.json_message(registration_ids=reg_ids, data=data)
  return resp
  

loop = asyncio.get_event_loop()
resp = loop.run_until_complete(response(reg_ids, data))
print(resp)
loop.close()
```


## Licensing
See [LICENSE](https://github.com/baris-erdem/asyncgcm/blob/master/LICENSE)
