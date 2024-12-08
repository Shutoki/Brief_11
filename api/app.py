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
import json
from api import client
# from extraction_ai import start_llm

app = Flask(__name__)

app.logger.setLevel(logging.DEBUG)

def fetch_offers(start, end, delta, all_jobs):

    new_start_dt = copy(start)

    while new_start_dt < end: 
        time.sleep(10)
        new_end_dt = new_start_dt + delta
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
            num_results = 0
        except Exception as e :
            print("Error !!!!!!!!!!!!!!!!")
            print(e)
            print(type(e))
            num_results = 0
        
        if num_results > 149:
            print(f"Too much results : {num_results}")
            delta = delta / 2 
            continue
        else:
            print(f"{num_results} resultats collectés")
            all_jobs += results
            new_start_dt = new_end_dt
            
        insert_datas(all_jobs)

def insert_datas(all_jobs):
    df = pd.DataFrame(all_jobs)

    for column in df.columns: 
        if df[column].apply(lambda x: isinstance(x, (dict, list))).any(): 
            df[column] = df[column].apply(lambda x: json.dumps(x))
    # print(df.iloc[5])

    columns_in_table = ["id", "intitule", "description", "dateCreation", "dateActualisation", "lieuTravail_latitude", "lieuTravail_longitude", "lieuTravail_libelle", "romeCode", "typeContrat", "experienceExige", "alternance", "origineOffre_urlOrigine", "dureeTravailLibelleConverti", "competences", "qualitesProfessionnelles", "formations"] 
    for column in df.columns: 
        if column not in columns_in_table: 
            df = df.drop(columns=[column])
    
    engine = create_engine('postgresql://admin:password@postgres_container:5432/france_travail_clean')
    table_name = 'france_travail'
    df.to_sql(table_name, engine, if_exists='replace', index=False)
    print("Données envoyées avec succès dans la bdd")
            
@app.route('/api/offers', methods=['POST']) 
def get_offers(): 
    data = request.get_json()
    # print(data)

    if "begin_datetime" not in data:
        return jsonify({'error' : 'No date_time provided'}), 400
    
    try:
        dt = datetime.fromisoformat(data['begin_datetime'])
        dt += timedelta(seconds=1)
    except ValueError:
        return jsonify({'error': 'Invalid datetime format'}), 400

    all_results = []
    start_dt = dt
    end_dt = datetime.today()
    delta = timedelta(days=10) 
    fetch_offers(start_dt, end_dt, delta, all_results) 
        
    return jsonify({'data': all_results})    


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)  
    # from datetime import datetime, timedelta # Définir les paramètres de test 
    # data = {"begin_datetime": "2024-11-25T00:00:00"} 
    # dt = datetime.fromisoformat(data['begin_datetime']) + timedelta(seconds=1) 
    # all_results = [] 
    # start_dt = dt 
    # end_dt = datetime.today() 
    # delta = timedelta(days=10) 
    # fetch_offers(start_dt, end_dt, delta, all_results) 
    # insert_datas(all_results) 
    # print(all_results)     

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

