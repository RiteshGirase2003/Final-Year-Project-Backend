from flask import jsonify

def updateMultimeter(DB, updated_data, model):
    try:
        existing_multimeter = DB.find_one({'model': model})
        if not existing_multimeter:
            return jsonify({'error': 'Multimeter not found'}), 404
        
        result = DB.update_one(
            {'model': model},
            {'$set': updated_data}
        )
        cnt = result.matched_count
        if cnt > 0:
            return jsonify({'message': 'Multimeter updated successfully'}), 200
        else:
            return jsonify({'error': 'Multimeter not found'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500
