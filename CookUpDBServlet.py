import web
import json
import logging

import MealMatcher

urls = (
    "/CookUpDB", "CookUpDBServlet"
)

format_string = '%(asctime)s %(funcName)s:%(lineno)s %(levelname)s - %(message)s'
logging.basicConfig(filename='/tmp/CookUpDBServlet.log',level=logging.DEBUG, format=format_string)

class CookUpDBServlet(object):
    def __init__(self):
        self.log = logging.getLogger()
        self.matcher = MealMatcher.MealMatcher()

    def GET(self):
        web.header("Content-type", "application/json; charset=utf-8")
        in_json=None
        try:
            in_json=json.loads(web.data())
        except:
            web.OK()
            message = "not a valid JSON"
            self.log.error(message)
            return '{"log_msg":message}'

        found_meal = self.matcher.get_meal_offer(in_json['meal'], in_json['location'])

        web.OK()
        return json.dumps(found_meal)

    def POST(self):
        web.header("Content-type", "application/json; charset=utf-8")
        in_json=None
        try:
            in_json=json.loads(web.data())
        except:
            web.OK()
            message = "not a valid JSON"
            self.log.error(message)
            return '{"log_msg":message}'

        web.OK()
        return json.dumps(in_json)





if __name__ == "__main__":
        app = web.application(urls, globals())
        app.run()
