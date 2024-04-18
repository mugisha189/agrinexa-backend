import requests
from decouple import config
def get_thingspeak_data(num_results=1):
    channel_id = config("THING_SPEAK_CHANNEL")
    read_api_key = config("THING_SPEAK_API")
    url = f'https://api.thingspeak.com/channels/{channel_id}/feeds.json'
    params = {'api_key': read_api_key, 'results': num_results}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  
        data = response.json()
        if 'feeds' in data:
            return data['feeds']
        else:
            return None  
    except requests.exceptions.RequestException as e:
        print(f"Error fetching ThingSpeak data: {e}")
        return None