import re
from flask import jsonify

def getAllMultimeters(DB):
    multimeters = []
    for multimeter in DB.find():
        multimeters.append({
            'id': str(multimeter['_id']),
            'name': multimeter['name'],
            'model': multimeter['model'],
            'description': multimeter['description'],
            'photo': multimeter['photo'],
            'screen_photo': multimeter['screen_photo']
        })
    return jsonify(multimeters)




def getMultimeterByModel(DB, model):
    multimeters = DB.find({'model': {'$regex': re.compile(model, re.IGNORECASE)}})
    
    multimeter_list = list(multimeters)
    
    if multimeter_list:  
        results = []
        for multimeter in multimeter_list:
            results.append({
                'id': str(multimeter['_id']),
                'name': multimeter['name'],
                'model': multimeter['model'],
                'description': multimeter['description'],
                'photo': multimeter['photo'],
                'screen_photo': multimeter['screen_photo']
            })
        
        return jsonify(results)  
    else:
        return jsonify({'error': 'Multimeter not found'}), 404
