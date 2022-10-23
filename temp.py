import csv
from app import HarmonisedSystem, db, Country, TradeFlow

# HS
# input_file = csv.DictReader(open("harmonized-system.csv"))
# for idx, row in enumerate(input_file):
#     section = row['section']
#     code = row['hscode']
#     description = row['description']
#     parent = row['parent']
#     level = row['level']
#
#     new_hs = HarmonisedSystem(section, code, description, parent, level)
#
#     print(f"Adding {new_hs}")
#     db.session.add(new_hs)
#     if idx % 100 == 0:
#         db.session.commit()
#         print(f"Finishing {new_hs}")

# Country
country_file = csv.DictReader(open("all.csv"))
for idx, row in enumerate(country_file):
    try:

        name = row['name']
        alpha2 = row['alpha-2']
        alpha3 = row['alpha-3']
        code = row['country-code']
        iso_3166_2 = row['iso_3166-2']
        region = row['region']
        region_code = row['region-code']

        new_country = Country(name, alpha2, alpha3, code, iso_3166_2, region, region_code)

        print(f"Adding {new_country} {idx}")
        db.session.add(new_country)
        db.session.commit()
        if idx % 10 == 0:

            print(f"Finishing {new_country}")
    except Exception as e:
        print(e)
        continue


# Trade
# trade_file = csv.DictReader(open("all_trade.csv"))
# for idx, row in enumerate(trade_file):
#     try:
#         if row['Year'] and row['Trade Flow'] and row['Netweight (kg)']:
#             year = row['Year']
#             flow = row['Trade Flow']
#             country_code = row['Reporter']
#             hs_code = row['Commodity Code']
#             qty = row['Qty']
#             qty_unit = row['Qty Unit']
#             net_weight = row['Netweight (kg)']
#             value = row['Trade Value (US$)']
#
#             new_trade = TradeFlow(year, flow, country_code, hs_code, qty, qty_unit, net_weight, value)
#
#             db.session.add(new_trade)
#             if idx % 100 == 0:
#                 print(f"Commiting {idx}")
#                 db.session.commit()
#     except Exception as e:
#         db.session.rollback()
#         print(e)
#         continue

