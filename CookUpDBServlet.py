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
        self.matcher = MealMatcher.MealMatcher()
        self.db_mockup = DBMockUp.DBMockUp()

    def GET(self):
        web.header("Content-type", "application/json; charset=utf-8")
        in_json=None
        try:
            in_json=json.loads(web.data())
        except:
            web.internalerror()
            message = "not a valid JSON"
            self.log.error(message)
            return '{"log_msg":message}'

        found_meal = self.matcher.get_meal_offer(in_json['meal'], in_json['location'])

        web.OK()
        self.log.debug('found meals: %s' % found_meal)
        return json.dumps(found_meal)

    def POST(self):
        self.log.debug('post')
        web.header("Content-type", "application/json; charset=utf-8")
        in_json=None
        try:
            in_json=json.loads(web.data())
        except:
            web.internalerror()
            message = "not a valid JSON"
            self.log.error(message)
            return '{"log_msg":message}'

        # check if it's create (no buyer yet) or edit (buyer available)
        edit = True if in_json['buyer'] else False

        if edit:
            self.close_order(in_json)
        else:
            self.create_order(in_json)

        web.OK()
        return json.dumps(in_json)

    def close_order(self, in_json):
        order = self.db_mockup.set_order_buyer(in_json['user'],in_json['buyer']) 
        self.log.debug('closed order: %s' % order)
        

    def create_order(self, in_json):
        self.db_mockup.create_order(in_json)
        self.log.debug('create order: %s' % in_json)

if __name__ == "__main__":
        app = web.application(urls, globals())
        app.run()
