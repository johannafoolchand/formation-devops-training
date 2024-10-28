import os
import sys
import json
from dotenv import load_dotenv
import ovh

# Load environment variables from .env file
load_dotenv()


# Retrieve values from environment variables
application_key = os.getenv('OVH_APPLICATION_KEY')
application_secret = os.getenv('OVH_APPLICATION_SECRET')
consumer_key = os.getenv('OVH_CONSUMER_KEY')


# Configuration
zone_name = 'pingsmash.fr'
sub = 'johanna'
subdomain = f'{sub}.{zone_name}'
record_id = '5323757454'
public_ip = '216.168.196.126'

# OVH API endpoint
ovh_endpoint = 'ovh-eu'

# Initialize OVH client
client = ovh.Client(
    endpoint=ovh_endpoint,
    application_key=application_key,
    application_secret=application_secret,
    consumer_key=consumer_key
)

print(f'Fetching record for {subdomain}')
result = client.get(f'/domain/zone/{zone_name}/record/{record_id}')
print(result)

print(f'Updating target record for {subdomain}')
print(f'Public IP = {public_ip}')

result = client.put(f'/domain/zone/{zone_name}/record/{record_id}',
    fieldType='A',
    subDomain=sub,
    target=public_ip,
    ttl=60
)
# print(result)

print(f'Refreshing zone {zone_name}')
result = client.post(f'/domain/zone/{zone_name}/refresh')

# print(result)
