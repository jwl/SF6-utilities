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

COOKIES = "CookieConsent={stamp:%27H+kbT3MrW7Jz7UDWRJZ/XAXATRAGlFm1ZE0lJThPTRgEapq8hnPSMA==%27%2Cnecessary:true%2Cpreferences:true%2Cstatistics:true%2Cmarketing:true%2Cmethod:%27explicit%27%2Cver:3%2Cutc:1712433407589%2Cregion:%27ca%27}; _ga_LZJGXR1W9E=GS1.1.1743264470.274.1.1743264471.0.0.0; _ga_4BKH6S3JTF=GS1.1.1743264470.139.1.1743264471.59.0.0; _ga=GA1.1.1988350405.1712693624; _ga_4BKH6S3JTF=deleted; __td_signed=true; _ga_B8S45G09HL=GS1.1.1736809966.13.1.1736810033.58.0.0; _gsid=e8776be1b1ca4d4b81aa5a0aede76eda; _tt_enable_cookie=1; _ttp=LIiV85VUR7DkC5eyX4s93yNhiDa.tt.1; _gcl_au=1.1.1228596969.1736441751; _td=a182f550-f748-47c1-8064-a9bd0df28cd4; buckler_r_id=b28a914c-5fc5-4371-94b9-a631ecbe5a59; buckler_id=EQ4PsPkd6IFwAaV5l8l2AIsf9ahx3LE9RPzBHtOV-HndB2vYoBZ5uhP8cDhgzmBb; buckler_praise_date=1743207776537"


def getHighestCharacterAndLP(character_league_infos):
    highestLPCharacter = ""
    highestLP = -2
    highestMRCharacter = ""
    highestMR = 0
    for character in character_league_infos:
        logging.debug(f"Investigating character {character['character_id']}, {character['character_name']}, LP for this character is {character['league_info']['league_point']}")
        if character['league_info']['league_point'] > highestLP:
            highestLP = character['league_info']['league_point']
            highestLPCharacter = character['character_name']
        if character['league_info']['master_rating'] > highestMR:
            highestMR = character['league_info']['master_rating']
            highestMRCharacter = character['character_name']

    logging.debug(f"Highest character is {highestLPCharacter} with LP of {highestLP}")
    if highestLP > 25000:
        logging.debug(f"Master character detected. Highest MR rated character for this account is {highestMRCharacter} at MR of {highestMR}")

    return (highestLPCharacter, highestLP, highestMRCharacter, highestMR)


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

    highestCharacter, highestLP, highestMRCharacter, highestMR = getHighestCharacterAndLP(data['response']['character_league_infos'])
    if highestLP < 25000:
        print(f"For CID {capcomId}, highest character is {highestCharacter} with LP of {highestLP}")
    elif highestMR > 0:
        print(f"For CID {capcomId}, highest character is {highestCharacter} with LP of {highestLP}.")
        print(f"Master rank detected! Highest MR character this season is {highestMRCharacter}, with MR of {highestMR}" )
    else:
        print(f"For CID {capcomId}, highest character is {highestCharacter} with LP of {highestLP}")
        print("Master rank detected! However, they have not played any games on their Master Ranked characters and have no MR this season." )
        


def main():
    parser = argparse.ArgumentParser(description='Looks up the highest rank for the given CID and the character that holds that rank.')
    parser.add_argument('capcomId', type=int, help='The CID (Capcom ID) to look up')
    args = parser.parse_args()
    retrieveLeagueInfo(args.capcomId)

if __name__ == '__main__':
    main()
