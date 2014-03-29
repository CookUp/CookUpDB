import DBMockUp
import pdb

class MealMatcher(object):

    def __init__(self):
        self.db = DBMockUp.DBMockUp()

    def get_meal_offer(self, meal_name, location):
        # meal not available
        orders=self.db.get_orders()
        matched_meals = [m for m in orders if m['meal']==self.get_meal_id(meal_name)]
        if len(matched_meals)==0:
            return None

        # no meal in this location
        matched_meals = [m for m in matched_meals if m['location']==location]
        if len(matched_meals)==0:
            return None

        return matched_meals


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
        
