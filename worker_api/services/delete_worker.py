from flask import jsonify

def deleteWorker(DB, reg_no):
    try:
        result = DB.delete_one({'Reg_No': reg_no})
        
        if result.deleted_count > 0:
            return jsonify({'message': 'Worker deleted successfully'}), 200
        else:
            return jsonify({'error': 'Worker not found'}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500
