from flask import jsonify

def updateWorker(DB, updated_data, reg_no):
    try:
        existing_worker = DB.find_one({'Reg_No': reg_no})
        if not existing_worker :
            return jsonify({'error': 'Worker not found'}), 404
        
        result = DB.update_one(
            {'Reg_No': reg_no},
            {'$set': updated_data}
        )
        cnt = result.matched_count
        if cnt > 0:
            return jsonify({'message': 'Worker updated successfully'}), 200
        else:
            return jsonify({'error': 'Worker not found'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500
