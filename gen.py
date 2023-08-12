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
        # The field 'youtube' almost always exists, and is usually the best link.
        link = next((x.get('link') for x in download_links if x.get('type').lower() == 'youtube'), None)
        # In a few cases, the link has a different name but it includes 'youtube'.
        if not link:
            link = next((x.get('link') for x in download_links if 'youtube' in x.get('type').lower()))

        if link:
            regex = r"(v=|v\/|embed\/|youtu.be\/)([^&#?\/]+)"
            match = re.search(regex, link)
            if match:
                return match.group(2)

        raise Exception("No youtube link found")

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
        10130, # A Place Called Universe
        10545, # Zoom 3
        10999, # fr-034 / hjb-104: time index
        11247, # Point Blank
        11282, # sota 2004 64k invitation
        11452, # Beyond
        1221, # fr-08: .the .product
        12790, # "Kings of the Playground" - Evoke 2004 64k invit
        12821, # Paradise
        13030, # The Prophecy - Project Nemesis
        14107, # hoodlum cracktro #1
        16326, # Binary Flow - The Assembly'05 Invitation
        17202, # hoodlum cracktro #3
        18252, # 195/95/256
        18339, # Che Guevara
        18342, # Fiat Homo
        24472, # Memento
        24476, # Ante Dominum
        24491, # Meet The Family
        25774, # Chaos Theory
        25776, # Dead Ringer
        25777, # Aesterozoa
        28479, # fr-052: platinum
        30055, # Frameskool - Breakpoint 2007 64k invit
        30637, # Outlined - Outline 2007 64k invitation
        5, # heaven seven
        50107, # Pimp My Spectrum
        50135, # Invoke
        51125, # Panic Room
        53646, # Transform
        53833, # ephemera
        53938, # Actuator
        54556, # imagine
        55146, # Haujobb BBQ 2010
        55300, # ino
        55535, # Behind the Curtain
        55546, # X Marks The Spot
        55550, # Ars Nova
        55587, # The Hungarian Gambit
        5569, # fr-019: poemtoahorse
        55737, # B - Incubation
        55991, # Insert No Coins
        56099, # 0 to X in Y
        56868, # Pandora
        56871, # We Have Accidently Borrowed Your Votedisk
        56877, # fr-080: Strobo-plus-32767: pacemaker
        57286, # chaos constructions 2011 invitation
        57449, # uncovering static
        58255, # Winner Intro
        58257, # Transplant
        58262, # epsilon
        59105, # The Scene Is Dead
        59106, # F - Felix's Workshop
        59107, # Gaia Machina
        59451, # qq
        59469, # Our drums can beat your moms'
        59918, # Wheels Within Wheels
        60278, # candy ~TokyoDemoFest 2013 Invitation~
        61204, # Turtles all the way down
        61206, # tensile
        61213, # A l'ancienne
        61721, # 905509
        61727, # Parallaxelerator
        62464, # luma
        62848, # Supermode
        62930, # Ooze
        62935, # the timeless
        63919, # hologram
        64170, # One of these days the sky's gonna break
        65336, # Small matters of the heart
        65342, # Offscreen Colonies
        65350, # on
        66297, # supervenience
        66495, # A+
        66748, # delight
        67106, # Darkness Lay Your Eyes Upon Me
        67113, # fermi paradox
        68147, # Universal Sequence
        68375, # Elysian
        69645, # Vessel
        69652, # Guberniya
        69654, # H - Immersion
        69658, # engage
        69669, # Eidolon
        7135, # Squish
        71570, # Yermom
        75713, # When Silence Dims The Stars Above
        77682, # Bros Before Foes
        78634, # trashpanda
        80996, # Atlas
        81015, # dope on wax
        81018, # The Jaderoom
        86224, # Smoothie
        88524, # Clean Slate
        88530, # Deus Cervidae
        88544, # Condition
        90435, # Domain
        90874, # astrophage (Black Valley 2022 invite)
        94135, # 0b5vr GLSL Techno Live Set
        9424, # fr-030: candytron
        9438, # Project Genesis
    ]

    # Comment if you want to fetch all prods (note that it will send lots of requests to pouet.net).
    ids = ids[0:5]

    for some_id in ids:
        prod_info = api.get_prod_info(some_id)
        print(json.dumps(prod_info, indent=4), ",")
