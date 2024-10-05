from flask import  jsonify
import re

def getWorker(DB):
    workers = []
    for worker in DB.find():
        workers.append({
            'id': str(worker['_id']),
            'name': worker['Name'],
            'reg_no': worker['Reg. No.'],
            'password': worker['password'],
            'photo': worker['photo']
        })
    return jsonify(workers)

def getWorkerById(DB,reg_no):
    workers = DB.find({'Reg_No': {'$regex': re.compile(reg_no, re.IGNORECASE)}})
    
    workers_list = list(workers)
    
    if workers_list: 
        results = []
        
        for worker in workers_list:
            results.append({
                'id': str(worker['_id']),
                'name': worker['Name'],
                'reg_no': worker['Reg_No'],
                'password': worker['password'],
                'photo': worker['photo']
            })
        
        return jsonify(results)  
    else:
        return jsonify({'error': 'Worker not found'}), 404

def getWorkerByName(DB,name):
    workers = DB.find({'Name': {'$regex': re.compile(name, re.IGNORECASE)}})
    
    workers_list = list(workers)
    
    if workers_list:  
        results = []
        for worker in workers_list:
            results.append({
                'id': str(worker['_id']),
                'name': worker['Name'],
                'reg_no': worker['Reg. No.'],
                'password': worker['password'],
                'photo': worker['photo']
            })
        
        return jsonify(results)  
    else:
        return jsonify({'error': 'Worker not found'}), 404