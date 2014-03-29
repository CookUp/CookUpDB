import json

class DBMockUp(object):

    def __init__(self):
        self.data=json.load(open('/home/volker/Dropbox/CookUp/DB.json'))

    def get_meals(self):
        return self.data['Meals']

    def get_orders(self):
        return self.data['Orders']

    def get_locations(self):
        return self.data['Locations']


