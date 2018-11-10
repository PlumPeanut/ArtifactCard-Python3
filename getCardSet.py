import json
import requests
import os

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

get_all_cardset()