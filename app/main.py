from typing import Optional,List

from fastapi import FastAPI, HTTPException
from fastapi.logger import logger
from fastapi.param_functions import Query

import pymysql
import os
import logging 
import random

DB_ENDPOINT = os.environ.get('db_endpoint')
DB_ADMIN_USER = os.environ.get('db_admin_user')
DB_ADMIN_PASSWORD = os.environ.get('db_admin_password')
DB_NAME = os.environ.get('db_name')


app = FastAPI(title='Query Service',version='0.1')
gunicorn_logger = logging.getLogger('gunicorn.error')
logger.handlers = gunicorn_logger.handlers
logger.setLevel(gunicorn_logger.level)


if __name__ != "main":
    logger.setLevel(gunicorn_logger.level)
else:
    logger.setLevel(logging.DEBUG)


def get_db_conn():
    try:
        conn = pymysql.connect(host=DB_ENDPOINT, user=DB_ADMIN_USER, passwd=DB_ADMIN_PASSWORD, db=DB_NAME, connect_timeout=5)
        return conn
    except pymysql.MySQLError as e:
        logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
        logger.error(e)
        raise



@app.get("/")
def read_root():
    return {"Service": "Ads"}


@app.get("/ads")
def ranking(advertiser_campaigns:str):
    # Split multiple values
    campaigns = [int(i) for i in advertiser_campaigns.split(",")]
    conn = get_db_conn()

    with conn.cursor(pymysql.cursors.DictCursor) as cursor:
        query = """SELECT campaign_id, id, headline, description, url FROM ads WHERE campaign_id IN %s"""
        cursor.execute(query,(campaigns,))
    
    if (results := cursor.fetchall()):
        ads = []
        ads_by_campaign = []

        for campaign in campaigns:
            ads_in_campaign = list(filter(lambda x: int(x['campaign_id'])==campaign,results))
            if ads_in_campaign:
                ads_by_campaign.append(ads_in_campaign)
        
        logger.error(ads_by_campaign)

        for group in ads_by_campaign:
            ads.append(random.choice(group))
        
        logger.error(ads)

        return ads
    else:
        raise HTTPException(status_code=404, detail= f'No se encontraron ads') 


