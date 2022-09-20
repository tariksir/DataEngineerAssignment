from flask import Flask, request
from .models import Covid19Stats

app = Flask("covid19_stats")
covid19_stats = Covid19Stats(url="https://api.covid19api.com/", time_period=30)
covid19_stats.init_data_miner()


@app.route("/status")
def get_status():
    return covid19_stats.get_api_status()


@app.route("/deathsPeak")
def get_deaths_peak() -> dict:
    if request.args.get("country") is None:
        return {"error": "country is required"}
    return covid19_stats.get_deaths_peak(request.args.get("country").capitalize())


@app.route("/CountryConfirmedMax")
def get_country_confirmed_max() -> dict:
    return covid19_stats.get_country_confirmed_max()
