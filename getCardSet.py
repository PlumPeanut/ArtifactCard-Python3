import json
import requests
import os


def create_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)


def make_get_request(request_url):
    response = requests.get(url=request_url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception('url error')


def stage1(setid):
    host = 'https://playartifact.com/cardset/'
    request_url = host + setid
    response = make_get_request(request_url)
    cdn_root = response['cdn_root']
    url = response['url']
    return cdn_root + url


def stage2(request_url):
    response = make_get_request(request_url)
    return response


def save_json(content, save_path):
    with open(save_path, 'w') as f:
        json.dump(content, f)


def save_cardset(setid):
    create_folder('save')
    state1_response = stage1(setid)  # a url to get full json
    state2_response = stage2(state1_response)  # full json of cardset
    save_json(state2_response, 'save/{}.json'.format(setid))
