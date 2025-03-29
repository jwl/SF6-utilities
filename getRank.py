import http.client
import json
import logging
import argparse

DEBUG = False

logging.basicConfig()
if DEBUG:
    logging.getLogger().setLevel(logging.DEBUG)
else:
    logging.getLogger().setLevel(logging.WARN)

COOKIES = "PASTE CONTENTS OF YOUR COOKIE HEADERS HERE"

def getHighestCharacterAndLP(character_league_infos):
    highestCharacter = ""
    highestLP = -2
    for character in character_league_infos:
        logging.debug(f"Investigating character {character['character_id']}, {character['character_name']}, LP for this character is {character['league_info']['league_point']}")
        if character['league_info']['league_point'] > highestLP:
            highestLP = character['league_info']['league_point']
            highestCharacter = character['character_name']

    logging.debug(f"Highest character is {highestCharacter} with LP of {highestLP}")

    return (highestCharacter, highestLP)


def retrieveLeagueInfo(capcomId: int):
    conn = http.client.HTTPSConnection('www.streetfighter.com')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:136.0) Gecko/20100101 Firefox/136.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': f'https://www.streetfighter.com/6/buckler/profile/{capcomId}/play',
        'Content-Type': 'application/json',
        'Origin': 'https://www.streetfighter.com',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Cookie': COOKIES,
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Priority': 'u=0',
        'TE': 'trailers',
    }
    json_data = {
        'targetShortId': capcomId,
        'targetSeasonId': -1,
        'locale': 'en',
        'peak': True,
    }
    conn.request(
        'POST',
        '/6/buckler/api/profile/play/act/leagueinfo',
        json.dumps(json_data),
        headers
    )
    response = conn.getresponse()
    data = json.loads(response.read())

    logging.debug(f"Buckler data retrieval response: {response.status}")

    highestCharacter, highestLP = getHighestCharacterAndLP(data['response']['character_league_infos'])
    print(f"For CID {capcomId}, highest character is {highestCharacter} with LP of {highestLP}")


def main():
    parser = argparse.ArgumentParser(description='Looks up the highest rank for the given CID and the character that holds that rank.')
    parser.add_argument('capcomId', type=int, help='The CID (Capcom ID) to look up')
    args = parser.parse_args()
    retrieveLeagueInfo(args.capcomId)

if __name__ == '__main__':
    main()
