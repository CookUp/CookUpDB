import json
import pdb

class DBMockUp(object):

    def __init__(self):
        self.db_filename='./DB.json'
        self.data=json.load(open(self.db_filename))

    def update_db_file(self):
        json.dump(self.data,open(self.db_filename,'w'),indent=4)

    def get_meals(self):
        return self.data['Meals']

    def get_orders(self):
        return self.data['Orders']

    def get_name_of(self, field_name, sub_field_name, ID):
        name = "NO NAME"
        for m in self.data[field_name]:
            if m['id']==ID:
                name=m[sub_field_name]
                break
        return name

    def set_order_buyer(self,ID,buyer):
        found = [o for o in self.data['Orders'] if o['id']==int(ID)]
        if len(found)==0:
            return False
        found[0]['buyer']=buyer
        self.update_db_file()
        return found[0]

    def get_locations(self):
        return self.data['Locations']

    def create_order(self, order):
        new_id = 1+max([o['id'] for o in self.get_orders()]) 
        order['id']=new_id
        self.data['Orders'].append(order)
        self.update_db_file()
        return order
        


