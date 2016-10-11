from bs4 import BeautifulSoup
from flask import Flask
import requests

app = Flask(__name__)

@app.route("/")
def getResults():
    page = requests.get("http://www.goduke.com/SportSelect.dbml?SPSID=22851&SPID=1850&DB_OEM_ID=4200&Q_SEASON=2016")
    # page = requests.get("http://www.goduke.com/SportSelect.dbml?SPSID=22851&SPID=1850&DB_OEM_ID=4200&Q_SEASON=2015")
    doc = BeautifulSoup(page.text, 'html.parser')

    results = doc.find_all("td", {"class" : "results"})
    opponents = doc.find_all("td", {"class" : "opponent"})
    venues = doc.find_all("td", {"class" : "time-location"})



    # Outcome of the game:
    # W = Duke Win
    # L = Duke Loss
    # C = Cancelled
    # P = Postponed

    last_result = results[-1].get_text().strip().split()
    if not results[0].get_text().strip().split():
        last_result = []
        last_outcome = "NOT YET"
        last_opponent = ""
    else:
        last_result = getLastResult(results, -1)
        last_outcome = last_result[0][0].upper()
        last_opponent = opponents[-1].get_text().strip()

    rv = last_outcome + "\n" + last_opponent
    return rv

def getLastResult(results, n):
    result = results[n].get_text().strip().split()
    if len(result) == 0:
        getLastResult(results, n - 1)
    return result


if __name__ == "__main__":
    app.run()