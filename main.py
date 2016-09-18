from bs4 import BeautifulSoup
from flask import Flask
import requests

app = Flask(__name__)

@app.route("/")
def getResults():
    page = requests.get("http://www.goduke.com/SportSelect.dbml?SPSID=22851&SPID=1850&DB_LANG=C&DB_OEM_ID=4200&Q_SEASON=2015")
    doc = BeautifulSoup(page.text, 'html.parser')

    results = doc.find_all("td", {"class" : "results"})
    opponents = doc.find_all("td", {"class" : "opponent"})
    venues = doc.find_all("td", {"class" : "time-location"})



    ###### Outcome of the game:
    ###### W = Duke Win
    ###### L = Duke Loss
    ###### C = Cancelled
    ###### P = Postponed
    last_result = results[-1].get_text().strip().split()
    last_outcome = last_result[0][0].upper()

    ###### Opponent
    last_opponent = opponents[-1].get_text().strip()

    ###### Did the game go into extras?
    if "(" in last_result:
        went_to_extras = True
    else:
        went_to_extras = False

    return last_outcome

if __name__ == "__main__":
    app.run()