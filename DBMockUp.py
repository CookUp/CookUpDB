import json

class DBMockUp(object):

    def __init__(self):
        self.db_filename='/home/volker/Dropbox/CookUp/DB.json'
        self.data=json.load(open(self.db_filename))

    def update_db_file(self):
        json.dump(self.data,open(self.db_filename,'w'),indent=4)

    def get_meals(self):
        return self.data['Meals']

    def get_orders(self):
        return self.data['Orders']

    def get_locations(self):
        return self.data['Locations']

    def create_order(self, order):
        new_id = 1+max([o['id'] for o in self.get_orders()]) 
        order['id']=new_id
        self.data['Orders'].append(order)
        self.update_db_file()
        


