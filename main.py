import datetime

import requests
from bs4 import BeautifulSoup as bs4

from flask import Flask
from flask_restful import Resource, Api


OYK_URL = "https://oulunkylanyhteiskoulu.fi/"


def get_food() -> list:
    with requests.Session() as s:
        g = s.get(OYK_URL)

    bs = bs4(g.text, 'html.parser')

    today = datetime.date.today().weekday()
    day = bs.select(".food__list")[today]

    foods = day.find_all("p")[1].text.split("\n",)
    clean_food = list(filter(None, foods))
    return clean_food


app = Flask(__name__)
api = Api(app)


class Food(Resource):
    def get(self):
        try:
            foods = get_food()
            alfred = {"items": [{"title": food}
                                for food in foods]}
            return alfred, 200
        except:
            return {}, 500


api.add_resource(Food, '/food')

if __name__ == "__main__":
    app.run(debug=True, port=5000)
