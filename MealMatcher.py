import DBMockUp
import pdb

class MealMatcher(object):

    def __init__(self, log):
        self.db = DBMockUp.DBMockUp()
        self.log = log

    def get_meal_offer(self, meal_name, location, cook):
        # meal not available
        filter_list = {
            'meal':meal_name,
            'location':location,
            'cook':cook
        }
        orders=self.db.get_orders()
        for k,v in filter_list.items():
            self.log.debug('filter %s for %s' % (k,v))
            orders = self.filter_orders(orders,k,v)
            if len(orders)==0:
                return []

        for i in range(len(orders)):
            orders[i]['mealName']=self.db.get_name_of('Meals','description',orders[i]['meal'])
            orders[i]['fileName']=self.db.get_name_of('Meals','name',orders[i]['meal'])
            orders[i]['cookName']=self.db.get_name_of('Users','name',orders[i]['cook'])
            orders[i]['locationName']=self.db.get_name_of('Locations','name',orders[i]['location'])

        return orders


        return orders

    def filter_orders(self, orders, filter_string, filter_id):
        self.log.debug('filter %s with %s: %s' %(orders,filter_string, filter_id))
        # filter is null
        if not filter_id:
            return orders

        filtered = []
        for o in orders:
            if filter_string not in o.keys():
                continue
            elif o[filter_string]!=self.get_meal_id(filter_id):
                continue
            elif o['buyer']:
                continue
            filtered.append(o)

        return filtered


    def get_meal_id(self, meal_name):
        meals = [m for m in self.db.get_meals() if m['id']==meal_name]
        if len(meals)==0:
            return -1
        return meals[0]['id']
        
    def get_location_id(self, location_name):
        locations = [m for m in self.db.get_locations() if m['id']==location_name]
        if len(locations)==0:
            return -1
        return locations[0]['id']
        
