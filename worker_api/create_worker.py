from flask import jsonify

def createWorker(DB, worker):
    try:
        existing_worker = DB.find_one({'Reg_No': worker['reg_no']})
        if existing_worker :
            return jsonify({'error': 'Worker already exists with this Reg. No.'}), 400
        
        DB.insert_one({
            'Name': worker['name'],
            'Reg_No': worker['reg_no'],
            'password': worker['password'],
            'photo': worker['photo']
        })
        
        return jsonify({'message': 'Worker created successfully'}), 201  

    except Exception as e:
        return jsonify({'error': str(e)}), 500  
