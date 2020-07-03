from flask import Flask, request, jsonify
from flask_restful import Api, Resource
import mysql.connector

mydb=mysql.connector.connect(
    host='localhost',
    user='root',
    password='root',
    database='Accounts'
)
mycursor = mydb.cursor()

app=Flask(__name__)
api=Api(app)

def ChangeUsers(res_json):
    list = res_json['users'].split(',')

    li = []
    for i in list:
	    li.append(int(i))
        
    res_json['users']=li
    return res_json

class AccInfo(Resource):

    def get(self, id):
        sql='SELECT * from acc WHERE id = %s'
        val_id = id
        mycursor.execute(sql, (val_id,))

        myresult=mycursor.fetchone()

        row_headers=[x[0] for x in mycursor.description]
        res_json=dict(zip(row_headers,myresult))
        
        return jsonify(ChangeUsers(res_json))

    def put(self, id):
        req_data = request.get_json()
        
        status=req_data['status']
        val_type=req_data['type']
        balance=req_data['balance']
        users_list=req_data['users']
        my_string = ','.join(map(str, users_list))

        sql='UPDATE acc SET status=%s, balance=%s, type=%s, users=%s WHERE id=%s'
        val = (status, balance, val_type, id, my_string)
        mycursor.execute(sql, val)
        mydb.commit()

    def delete(self, id):
        sql = 'DELETE from acc WHERE id = %s'
        mycursor.execute(sql, (id,))
        mydb.commit()

class PostCall(Resource):
    
    def post(self):
        req_data = request.get_json()

        acc_id=req_data['id']
        status=req_data['status']
        val_type=req_data['type']
        users_list=req_data['users']
        my_string = ','.join(map(str, users_list))  

        sql = 'INSERT INTO acc (id, users, status, balance, type) VALUES (%s, %s, %s, %s, %s)'
        val=(acc_id, my_string, status, 0, val_type)
        mycursor.execute(sql, val)
        mydb.commit()

        return jsonify(req_data)
    

class AllAcs(Resource):

    def get(self):
        all_acs=[]
        mycursor.execute("SELECT * FROM acc")
        row_headers=[x[0] for x in mycursor.description]
        myresult = mycursor.fetchall()
        for result in myresult:
            res_json = dict(zip(row_headers,result))

            all_acs.append(ChangeUsers(res_json))

        return jsonify(all_acs)

api.add_resource(AccInfo, '/acc/<int:id>')
api.add_resource(PostCall, '/acc')
api.add_resource(AllAcs, '/accs')

if __name__=='__main__':
    app.run(debug=True)