from flask import jsonify

def deleteMultimeter(DB, model):
    try:
        result = DB.delete_one({'model': model})
        
        if result.deleted_count > 0:
            return jsonify({'message': 'Multimeter deleted successfully'}), 200
        else:
            return jsonify({'error': 'Multimeter not found'}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500
