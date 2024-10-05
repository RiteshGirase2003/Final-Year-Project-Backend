from flask import jsonify

def createMultimeter(DB, multimeter):
    try:
        existing_multimeter = DB.find_one({'model': multimeter['model']})
        if existing_multimeter:
            return jsonify({'error': 'Multimeter already exists with this model.'}), 400
        
        DB.insert_one({
            'name': multimeter['name'],
            'model': multimeter['model'],
            'description': multimeter['description'],
            'photo': multimeter['photo'],
            'screen_photo': multimeter['screen_photo']
        })
        
        return jsonify({'message': 'Multimeter created successfully'}), 201  

    except Exception as e:
        return jsonify({'error': str(e)}), 500  
