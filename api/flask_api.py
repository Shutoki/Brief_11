import pandas as pd
import numpy as np
from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Sequence, DateTime, Float, Text
from sqlalchemy.orm import declarative_base
from sqlalchemy_utils import database_exists, create_database
from offres_emploi import Api
from offres_emploi.utils import dt_to_str_iso
from datetime import datetime, timedelta
import time
from copy import copy
import logging
from api import client

app = Flask(__name__)

app.logger.setLevel(logging.DEBUG)

def fetch_offers(start, end, delta, all_jobs):

    new_start_dt = copy(start)

    while start < end: 
        time.sleep(10)
        new_end_dt = end - delta
        print(f"date obtenues de {new_start_dt} à {new_end_dt}")
        results = []
        params = {
            "codeROME": "M1805",
            'minCreationDate': dt_to_str_iso(new_start_dt),
            'maxCreationDate': dt_to_str_iso(new_end_dt)
        }
        
        try: 
            search_on_big_data = client.search(params=params) 
            num_results = int(search_on_big_data["Content-Range"]["max_results"])
            # print(f"Test Response: {search_on_big_data}")
            results = search_on_big_data['resultats']
        except AttributeError:
            print("No results. Continue...")
        except Exception as e :
            print("Error !!!!!!!!!!!!!!!!")
            print(e)
            print(type(e))
            num_results = 0
        
        if num_results > 149:
            print(f"Too much results : {num_results}")
            fetch_offers(new_start_dt, new_end_dt, delta / 2, all_jobs)
        else:
            print(f"{num_results} resultats collectés")
            all_jobs += results
            new_start_dt += delta
            
           

#     params.update({'minCreationDate' : dt_to_str_iso(end_dt), 'maxCreationDate': dt_to_str_iso(start_dt)})
#     print(f"Params: {params}")

#     try:
#         test_params = {
#     "motsCles": ["M1805", "M1403"]
# }

#         search_on_big_data = client.search(params=test_params)
#         # print(f"Test Response: {search_on_big_data}")
#         results =  search_on_big_data['resultats']  
#     except AttributeError as e :
#         print(f"Erreur lors de l'appel API : {e}") 
#         return all_jobs

#     all_jobs.extend(results)
#     new_start_dt = end_dt 
#     new_end_dt = new_start_dt - diff_hour

#     if new_end_dt >= (datetime.today() - timedelta(days=2)): 
#         print("Arrêt des recherches : date limite J-2 atteinte.") 
#         return all_jobs 
        
#     if len(results) >= 150: 
#         fetch_offers(new_start_dt, new_end_dt, all_jobs) 
        
#     return all_jobs
        
@app.route('/api/offers', methods=['GET']) 
def get_offers(): 
    all_results = []
    start_dt = datetime.today() - timedelta(days=30)
    delta = timedelta(days=10) 
    end_dt = datetime.today()
    offers = fetch_offers(start_dt, end_dt, delta, all_results) 
    print(f"Total récupéré : {len(offers)}") 
    return jsonify(offers)

    # all_jobs = []
    # total_fetch = 0
    # page = 1
    # limit=150

    # while total_fetch < 20000:
    #     params.update({'page' : page, 'limit': limit})
        
    #     if not results:
    #         break

    #     all_jobs.append(results)
    #     total_fetch += len(results)

    #     print(f"Total récupéré : {total_fetch}")

    #     page += 1

    # return all_jobs

# engine = create_engine("postgresql://username:password@localhost/nomdetadatabase")

# if_exists = 'replace'

# with engine.connect() as con:
#     new_df.to_sql(
#         name="Job3", 
#         con=con,
#         if_exists=if_exists
#     )


        # params.update({'minCreationDate' : dt_to_str_iso(end_dt), 'maxCreationDate': dt_to_str_iso(start_dt)})
        # search_on_big_data = client.search(params=params)
        # results =  search_on_big_data['resultats']  
        # all_jobs.extend(results)
        # old_start_dt = start_dt
        # oneMonth = timedelta(days=30)
        # new_start_dt = end_dt 
        # new_end_dt = new_start_dt - diff_hour 
        # if new_end_dt < old_start_dt - oneMonth:
        #     fetch_offers(new_start_dt, new_end_dt, all_jobs)
        # return all_jobs 

if __name__ == "__main__":
    app.run(debug=True)