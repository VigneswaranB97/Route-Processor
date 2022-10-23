import json

import numpy as np
from flask import Flask, request
from flask_restful import Api
from sklearn.metrics.pairwise import cosine_similarity
import os
import pandas as pd
import ast

s = open('hs_vec.txt', 'r').read()
hs_vecs = ast.literal_eval(s)

with open('ImpExpTrade.json') as handle:
    imp_exp_dict = json.loads(handle.read())


# Program to measure the similarity between
# two sentences using cosine similarity.
# from nltk.corpus import stopwords
# from nltk.tokenize import word_tokenize

from sentence_transformers import SentenceTransformer
model_name = "bert-base-nli-mean-tokens"
model = SentenceTransformer(model_name)

# init app
app = Flask(__name__)
api = Api(app)
basedir = os.path.abspath(os.path.dirname(__file__))

def get_trade_details_helper(countries, year):
    all_resps = []
    total = {
        "export_cost": 0,
        "export_qty": 0,
        "import_cost": 0,
        "import_qty": 0
    }
    for country in countries:
        details = {}
        for code, data in imp_exp_dict[str(year)][str(country)].items():
            details[str(code)] = {
                "export_cost": 0,
                "export_qty": 0,
                "import_cost": 0,
                "import_qty": 0
            }

            for tc, val in data.items():
                details[code][tc] += val
                total[tc] += val

        all_resps.append({
            'year': year,
            'details': details,
            'country': country,
        })

    return {
        'total': total,
        'resp': all_resps
    }


@app.route('/get-trade-details', methods=['POST'])
def get_trade_details():
    try:
        year = request.json['year']
        countries = list(request.json['country'])
        if 'All' in countries:
            total = {
                "export_cost": 0,
                "export_qty": 0,
                "import_cost": 0,
                "import_qty": 0
            }
            countries_list = []
            for country in imp_exp_dict[str(year)].keys():
                countries_list.append(country)
            print(countries_list)
            resp = get_trade_details_helper(countries_list, year)
            return resp
        else:
            all_resps = []
            for country in countries:
                details = {}
                for code, data in imp_exp_dict[str(year)][str(country)].items():
                    details[str(code)] = {
                        "export_cost": 0,
                        "export_qty": 0,
                        "import_cost": 0,
                        "import_qty": 0
                    }

                    for tc, val in data.items():
                        details[code][tc] += val

                all_resps.append({
                    'year': year,
                    'country': country,
                    'details': details
                })
            return {
                'details': all_resps
            }
    except Exception as e:
        return {
            'error': e,
            'details': []
        }

@app.route('/get-hs', methods=['POST'])
def predict_hs():
    try:
        description = request.json['description']
        hs_df = pd.read_csv('harmonized-system.csv')
        vector = model.encode(description)

        dataSetII = []
        for i in hs_vecs.values():
            dataSetII.append(np.array(i))

        all_hs_sentences = sorted(hs_df['description'].unique())
        cos_sims = list(cosine_similarity([vector], np.array(dataSetII)))
        if len(cos_sims) > 0:
            all_results = []
            for idx, cs in enumerate(list(cos_sims[0])):
                all_results.append([all_hs_sentences[idx], cs, hs_df[hs_df['description'] == str(all_hs_sentences[idx])]['hscode'].values[0]])
            cos_sims = sorted(all_results, key=lambda res: res[1], reverse=True)[:15]
            return {
                'hs_codes': str(cos_sims)
            }
        else:
            return {
                'hs_codes': []
            }
    except Exception as e:
        return {
            'error': e,
            'hs_codes': []
        }


# Run server
if __name__ == "__main__":
    app.run(debug=True)
