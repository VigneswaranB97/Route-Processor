# Route-Processor
Optimal Route finder

The sudden booming growth of cross-border e-commerce has posed various challenges to both sellers and consumers. 
For eCommerce, B2B shipments can have small order quantities and a low merchandise value, while B2C shipments tend to be highly variable and very small, with many falling below the minimum threshold for taxes and duties.

## Technologies
Project is created with:
* Python 3.6+
* NLP (Transformers)
* Pandas
* Numpy
* Linear Programming
* Operational research

## Installation Procedure and To run Flask Server
Download Submitted zip file or clone the repo
```
$ pip3 install -r requirements.txt
$ python3 app.py
```

### Request Example
`POST /get-hs`

```
curl --location --request POST 'http://localhost:5000/get-hs' \
--header 'Content-Type: application/json' \
--data-raw '{
    "description": "Kit Kat is a chocolate-covered wafer bar confection created by Rowntree'\''s of York, United Kingdom, and is now produced globally by Nestlé"
}'
```

### Response
```
{
    "hs_codes": "[['Chocolate and other food preparations containing cocoa; n.e.c. in chapter 18', 0.8189862655702076, '180690'], ['Chocolate and other food preparations containing cocoa', 0.7453580079949778, '1806'], ['Machinery; industrial, for the manufacture of confectionery, cocoa or chocolate', 0.7399847297726326, '843820'], ['Chocolate and other food preparations containing cocoa; in blocks, slabs or bars, filled, weighing 2kg or less', 0.7347044741623772, '180631'], ['Yogurt; buttermilk, curdled milk and cream, kephir and other fermented or acidified milk and cream, whether or not concentrated or containing added sugar or other sweetening matter or flavoured or containing added fruit, nuts or cocoa.', 0.7052670893009947, '0403'], ['Food preparations; waffles and wafers, whether or not containing cocoa', 0.7037783564048795, '190532'], [\"Food preparations; bakers' wares n.e.c. in heading no. 1605, whether or not containing cocoa; communion wafers, empty cachets suitable for pharmaceutical use, sealing wafers, rice papers and similar products\", 0.6891357849411335, '190590'], ['Dairy produce; buttermilk, curdled milk or cream, kephir, fermented or acidified milk or cream, whether or not concentrated or containing added sweetening, flavouring, fruit, nuts or cocoa (excluding yoghurt)', 0.6885271129955641, '040390'], ['Dairy produce; yoghurt, whether or not concentrated or containing added sugar or other sweetening matter or flavoured or containing added fruit, nuts or cocoa', 0.6837901729443461, '040320'], ['Food preparations; gingerbread and the like, whether or not containing cocoa', 0.6809614826702766, '190520'], ['Food preparations; crispbread, whether or not containing cocoa', 0.6758505330493845, '190510'], ['Chocolate and other food preparations containing cocoa; in blocks, slabs or bars, (not filled), weighing 2kg or less', 0.6719437179270165, '180632'], ['Jams, fruit jellies, marmalades, purees and pastes; of fruit or nuts n.e.c. in heading no. 2007, cooked preparations (excluding homogenised), whether or not containing added sugar or other sweetening matter', 0.6712953516442957, '200799'], ['Cocoa and cocoa preparations', 0.6698023614602358, '18'], ['Chocolate & other food preparations containing cocoa; in blocks, slabs or bars weighing more than 2kg or in liquid, paste, powder, granular or other bulk form in containers or immediate packings, content exceeding 2kg', 0.6689912416258638, '180620']]"
}
```
