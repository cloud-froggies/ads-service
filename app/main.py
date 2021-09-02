from fastapi import FastAPI, Query
from typing import List
from typing import Optional
import random

app = FastAPI()


@app.get("/ads")
def ranking(advertiser_campaigns: str):
    # Split multiple values
    campaigns = [int(i) for i in advertiser_campaigns.split(",")]

    # Random ad per campaign
    ads = []
    query = "SELECT campaign_id, id, headline, description, url FROM ads WHERE campaign_id IN {}".format(tuple(campaigns))
    

    

    return ads



