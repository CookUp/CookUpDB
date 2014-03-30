import pdb
import sys
import web
import json
import logging

import MealMatcher
import DBMockUp

urls = (
    "/CookUpDB", "CookUpDBServlet"
)

format_string = '%(asctime)s %(funcName)s:%(lineno)s %(levelname)s - %(message)s'
logging.basicConfig(filename='/tmp/CookUpDBServlet.log',level=logging.DEBUG, format=format_string)#,stream=logging.StreamHandler(sys.stdout))

class CookUpDBServlet(object):
    def __init__(self):
        self.log = logging.getLogger()
        self.matcher = MealMatcher.MealMatcher(self.log)
        self.db_mockup = DBMockUp.DBMockUp()

        self.actions = {
            1:self.search_meal,
            2:self.create_order,
            3:self.close_order,
        }

    def POST(self):
        web.header("Content-type", "application/json; charset=utf-8")
        in_json=None
        in_data=web.data()
        try:
            in_json=json.loads(in_data)
        except:
            return self.return_error("not a valid JSON: %s" % in_data)
        self.log.debug('received JSON: %s' % in_json)

        # check if it's create (no buyer yet) or edit (buyer available)
        if 'action' not in in_json:
            return self.return_error('action not in json' % in_json)
        if 'data' not in in_json or len(in_json['data'])==0:
            return self.return_error('data not in json' % in_json)

        action_id=int(in_json['action'])

        if action_id not in self.actions:
            return self.return_error("not a valid action: %s" % action_id)

        self.log.debug('action: %s' % action_id)
        out = {"nothing":"done"}
        try:
            out = self.actions[action_id](in_json['data'])
        except Exception,e:
            print e
            return self.return_error('action failed, reason: %s' % e)

        web.OK()
        return json.dumps(out)

    def return_error(self, message):
        web.notfound()
        self.log.error(message)
        return '{"log_msg":"%s"}' % message

    def search_meal(self,in_json):
        for kl in ['meal','location','cook']:
            if kl not in in_json:
                raise Exception('JSON not complete, %s missing' % kl)
                
        self.log.debug('search for meal: %s' % in_json)
        found_meal = self.matcher.get_meal_offer(in_json['meal'], in_json['location'], in_json['cook'])
        self.log.debug('found meals: %s' % found_meal)
        return found_meal

    def create_order(self, in_json):
        self.log.debug('create order: %s' % in_json)
        created_order = self.db_mockup.create_order(in_json)
        self.log.debug('created order: %s' % created_order)
        return created_order

    def close_order(self, in_json):
        self.log.debug('close order: %s' % in_json)
        closed_order = self.db_mockup.set_order_buyer(in_json['id'],in_json['buyer']) 
        self.log.debug('closed order: %s' % closed_order)
        return closed_order

if __name__ == "__main__":
        app = web.application(urls, globals())
        app.run()
