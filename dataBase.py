import pymongo
import json
from getCardSet import get_setids, default_setids_path

port = 27017
username = None
password = None
client = pymongo.MongoClient(host='localhost', port=27017)
db = client['artifact']


def load_cardset(setid):
    with open('save/' + setid + '.json') as f:
        cardset = json.load(f)
        return cardset


def extract_cardset_info(cardset_json):
    cardset_info = cardset_json['set_info']
    set_id = cardset_info['set_id']
    set_name = cardset_info['name']['english']
    return set_id, set_name


setids = get_setids(default_setids_path)
for set_id in setids:
    cardset = load_cardset(set_id)['card_set']
    set_id, set_name = extract_cardset_info(cardset)
    collection = db[str(set_id)]
    card_list = cardset['card_list']
    for card in card_list:
        collection.insert_one(card)
