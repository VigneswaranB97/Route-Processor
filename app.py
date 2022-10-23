import enum
import json

import numpy as np
from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
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

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:Actioulnozmsql@127.0.0.1:3306/commerce"
# "mysql://admin:yashu123@pareto-gets.cm3wnhjolb5v.us-east-1.rds.amazonaws.com:3306/commerce"
# mysql://root:Actioulnozmsql@127.0.0.1:3306/commerce
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init DB
db = SQLAlchemy(app)

# Init marshmallow
ma = Marshmallow(app)

class TradeFlowEnum(enum.Enum):
    Import = 'Import'
    Export = 'Export'

class TradeFlow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, nullable=False)
    flow = db.Column(db.Enum(TradeFlowEnum), nullable=False)
    country_code = db.Column(db.String(100), nullable=False)
    hs_code = db.Column(db.String(20), nullable=False)
    qty = db.Column(db.BigInteger, nullable=False)
    qty_unit = db.Column(db.String(50), nullable=False)
    net_weight = db.Column(db.BigInteger, nullable=False)
    value = db.Column(db.BigInteger, nullable=False)

    def __init__(self, year, flow, country_code, hs_code, qty, qty_unit, net_weight, value):
        self.year = year
        self.flow = flow
        self.country_code = country_code
        self.hs_code = hs_code
        self.qty = qty
        self.qty_unit = qty_unit
        self.net_weight = net_weight
        self.value = value

    def __str__(self):
        return f"{self.year}, {self.flow}, {self.country_code}, {self.hs_code}, {self.qty}, {self.net_weight}, {self.value}"

class Country(db.Model):
    name = db.Column(db.String(100), primary_key=True, nullable=False)
    alpha2 = db.Column(db.String(10), nullable=False)
    alpha3 = db.Column(db.String(10), nullable=False)
    code = db.Column(db.Integer, nullable=False)
    iso_3166_2 = db.Column(db.String(100), nullable=False)
    region = db.Column(db.String(100), nullable=False)
    region_code = db.Column(db.Integer, nullable=False)

    def __init__(self, name, alpha2, alpha3, code, iso_3166_2, region, region_code):
        self.name = name
        self.alpha2 = alpha2
        self.alpha3 = alpha3
        self.code = code
        self.iso_3166_2 = iso_3166_2
        self.region = region
        self.region_code = region_code

    def __str__(self):
        return f"{self.name}, {self.alpha2}, {self.alpha3}, {self.code}, {self.iso_3166_2}"

class HarmonisedSystem(db.Model):
    section = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(20), nullable=False, primary_key=True, unique=True)
    description = db.Column(db.String(500), nullable=False)
    parent = db.Column(db.String(100), nullable=False)
    level = db.Column(db.Integer, nullable=False)

    def __init__(self, section, code, description, parent, level):
        self.section = section
        self.code = code
        self.description = description
        self.parent = parent
        self.level = level

    def __str__(self):
        return f"{self.section}, {self.code}, {self.description}, {self.parent}, {self.level}"

class HarmonisedSystemSchema(ma.Schema):
    class Meta:
        fields = ('id', 'section', 'code', 'description', 'parent', 'level')

# Init schema
hs_schema = HarmonisedSystemSchema()
hs_schemas = HarmonisedSystemSchema(many=True)

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
