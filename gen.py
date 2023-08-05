import json
import re
import requests

class PouetAPIWrapper:
    base_url = "https://api.pouet.net/v1/prod/"

    def __init__(self):
        pass

    def extract_group_names(self, groups):
        group_names = [group.get('name') for group in groups]
        return ' and '.join(group_names)
    
    def find_youtube_id(self, download_links):
        # TODO: use heuristics to find the best link (e.g. "youtube" vs "youtube (final)")
        for link in download_links:
            if link.get('type').lower() == 'youtube':
                # regex = r"?v=([a-zA-Z0-9]*)"
                regex = r"(v=|v\/|embed\/|youtu.be\/)([^&#?\/]+)"
                match = re.search(regex, link.get('link'))
                if match:
                    return match.group(2)

    def get_prod_info(self, prod_id):
        url = f"{self.base_url}?id={prod_id}"

        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes

            data = response.json()
            prod = data.get('prod', {})
            return {
                'pouet': prod.get('id'),
                'title': prod.get('name'),
                'group': self.extract_group_names(prod.get('groups')),
                'youtube': self.find_youtube_id(prod.get('downloadLinks')),
                'date': prod.get('releaseDate'),
                'screenshot': prod.get('screenshot'),
                'demozoo': prod.get('demozoo', {}),
            }
        
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from the API: {e}")
            return {}

if __name__ == "__main__":
    api = PouetAPIWrapper()
    ids = [
        59106, # F - Felix's Workshop
        65342, # Offscreen Colonies
        62935, # the timeless
        67113, # fermi paradox
        67106, # Darkness Lay Your Eyes Upon Me
        61204, # Turtles all the way down
        88524, # Clean Slate
    ]

    for some_id in ids:
        prod_info = api.get_prod_info(some_id)
        print(json.dumps(prod_info, indent=4), ",")
