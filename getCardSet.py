import json
import requests
import os
from urllib import request

default_setids_path = 'setid'


def create_folder(path: str):
    """
    Create folder if path doesn't exist
    :param path:File path you want to create
    :return:None
    """
    if not os.path.exists(path):
        os.makedirs(path)


def make_get_request(request_url: str) -> dict:
    """
    Send a get request to host
    :param request_url: Url you want to request
    :return:Json file if succeed
    """
    response = requests.get(url=request_url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception('url error')


def stage1(setid: str) -> str:
    """
    State1 in official Card Set API
    :param setid: Cardset id
    :return: A url for state2
    """
    host = 'https://playartifact.com/cardset/'
    request_url = host + setid
    response = make_get_request(request_url)
    cdn_root = response['cdn_root']
    url = response['url']
    return cdn_root + url


def stage2(request_url: str) -> dict:
    """
    State2 in official Card Set API
    :param request_url: Url from stage1
    :return:Json file of cardset information
    """
    response = make_get_request(request_url)
    return response


def save_json(content: dict, save_path: str):
    """
    Save dict to json
    :param content: dict object
    :param save_path: output path
    :return:None
    """
    with open(save_path, 'w') as f:
        json.dump(content, f)


def save_cardset(setid: str):
    """
    Save cardset information to local file
    :param setid: cardset id
    :return:None
    """
    create_folder('save')
    state1_response = stage1(setid)  # a url to get full json
    state2_response = stage2(state1_response)  # full json of cardset
    save_json(state2_response, 'save/{}.json'.format(setid))


def get_setids(file_path: str) -> list:
    """
    Get all possible cardset id
    :param file_path: Local file which stores all cardset id
    :return:List. All cardset id
    """
    setids = []
    with open(file_path) as f:
        lines = f.readlines()
    for line in lines:
        setids.append(line.strip())
    return setids


def get_all_cardset():
    """
    Store all possible cardset to local file
    :return:None
    """
    setids = get_setids(default_setids_path)
    for setid in setids:
        save_cardset(setid)


def check_url(value):
    if not isinstance(value, dict):
        if isinstance(value, str):
            if 'http' in value:
                path = 'img/' + value.split('/')[-1]
                if not os.path.exists(path):
                    request.urlretrieve(value, path)
    else:
        for key in value:
            check_url(value[key])


def download_images():
    setids = get_setids(default_setids_path)
    for set_id in setids:
        with open('save/' + set_id + '.json') as f:
            cardset = json.load(f)['card_set']
        card_list = cardset['card_list']
        for card in card_list:
            check_url(card)

# get_all_cardset()
download_images()