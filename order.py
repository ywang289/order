from flask import Flask, Response, request,flash, render_template, make_response, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import json
from datetime import datetime


app=Flask(__name__)
CORS(app)

app.config['SECRET_KEY']='zy112612' # 密码
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://admin:zy112612@e6156-1.cudpmdtzmg9e.us-east-1.rds.amazonaws.com:3306/Purchase'
    # 协议：mysql+pymysql
    # 用户名：root
    # 密码：2333
    # IP地址：localhost
    # 端口：3306
    # 数据库名：runoob #这里的数据库需要提前建好
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']=True
db=SQLAlchemy(app)

#测试连上
with app.app_context():
    sql = 'select * from Contains'
    result = db.session.execute(sql)
    print(result.fetchall())


@app.route('/', methods=['GET'])
def home():
    return 'Hello World!'

# {"oid":"1"}
@app.route('/customer/order_details', methods=['POST'])
def order_detail():
    if request.method == 'POST':
        data = json.loads(request.get_data())
        oid = data['oid']
        print(oid)
        sql = 'SELECT c.mid, c.numbers FROM Contains c WHERE c.oid = {}'.format(oid)
        result = db.session.execute(sql).fetchall()
        # json_list=[]
        answer={}
        
        for row in result:
            # print("new row")
            answer[row[0]]= row[1]
            # print(len(row))
            # json_list.append([x for x in row]) 

    return answer

# /order/add_merchandise
# data format from front-end to back-end
# 	{email, name, price, remaining_amount, description, picture, mid}
# <actually need mid>
# data format from backend to front-end
# 	{response: succeed or fail}

# INSERT INTO Merchandises VALUES (‘{}’)
# placeholder: mid

@app.route('/order/add_merchandise', methods=['POST'])
def delete_merchandise():
    response={}
    if request.method == 'POST':
        data = json.loads(request.get_data())
        
        mid= data["mid"]
        
        try:
            sql="INSERT INTO Merchandises VALUES ('{}')".format(mid)
            db.session.execute(sql)
            
        except Exception as err:
            print("order")
            return {"message": "error! change information error","state":False}  
        response["message"]= True
        response['state']= True
    return response

# @app.route('/order/delete_merchandise', methods=['POST'])
# def delete_merchandise():
#     if request.method == 'POST':
#         data = json.loads(request.get_data())
#         oid = data['O']
#         sql = ''
#         result = db.session.execute(sql).fetchall()
#         json_list=[]
#         for row in result:
#             json_list.append([x for x in row])       

#     return json_list
        

# { "email":"test3@gmail.com", "timestamp":"2022-12-14 17:30:00" ,"order":{"1":"10", "10":"2"}, "oid":"4"}

@app.route('/order/place_order', methods=['POST'])
def place_order():
# {email: string
# timestamp: time, (current time)
# order: dictionary{mid: numbers}
# oid: comes from customer/place_order}

    response={}
    if request.method == 'POST':
        data = json.loads(request.get_data())
        email= data['email']
        timestamp= data["timestamp"]
        order= data['order']
        oid= data['oid']
        print(oid)
#       insert into Orders values (‘{}’) placeholder is oid
        try:
            sql="INSERT INTO Orders VALUES ('{}')".format(oid)
            db.session.execute(sql)
        except Exception as err:
            print("order")
            return {"message": "error! change information error","state":False}

#         for each (mid,numbers) in dictionary:
#   insert into Contains values (‘{}’, ‘{}’, ‘{}’)
# placeholder: oid, mid, numbers
        for (mid, numbers) in order.items():
            print(mid)
            print(numbers)
            try:
                sql="INSERT INTO Contains VALUES ('{}', '{}', '{}')".format(oid, mid, numbers)
                db.session.execute(sql)
            except Exception as err:
                print("contains")
                return {"message": "error! change information error","state":False}
           
        response["message"]= True
        response['state']= True
    return response
        

if __name__=='__main__':
    app.run(host='0.0.0.0', port=8082, debug=True)