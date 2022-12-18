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
        try:
            sql = "SELECT c.mid, m.name, c.numbers FROM Merchandises m, Contains c WHERE c.oid = '{}' AND c.mid = m.mid".format(oid)
            result = db.session.execute(sql).fetchall()
        except Exception as err:
            return {"state": False, "message": "error! input error"}
        json_list=[]
        
        for row in result:
            # print("new row")
            answer={}
            answer["mid"]= row[0]
            answer["name"]= row[1]
            answer["amount"]= row[2]
            json_list.append(answer)
            
            # print(len(row))
            # json_list.append([x for x in row]) 

    return {"data": json_list}



@app.route('/order/add_merchandise', methods=['POST'])
def delete_merchandise():
    response={}
    if request.method == 'POST':
        data = json.loads(request.get_data())
        
        mid= data["mid"]
        name= data["name"]
        print ("mid")
        print(mid)
        print("name")
        print (name)
        
        try:
            sql="INSERT INTO Merchandises VALUES ('{}','{}')".format(mid,name)
            db.session.execute(sql)
            
        except Exception as err:
            print("order")
            return {"message": "error! change information error","state":False}  
        response["message"]= True
        response['state']= True
    return response

#<actually need mid, name>
@app.route('/order/update_merchandise', methods=['POST'])
def update_merchandise():
    response={}
    if request.method == 'POST':
        data = json.loads(request.get_data())
        
        mid= data["mid"]
        name= data["name"]
        
        try:
            sql="UPDATE Merchandises SET Name = '{}' WHERE mid = '{}'".format(name, mid)
            db.session.execute(sql)
            
        except Exception as err:
            print("order")
            return {"message": "error! change information error","state":False}  

        response["message"]= True
        response['state']= True

    return response

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
        items= data['items']
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
        for i in range(len(items)):
            
            try:
                sql="INSERT INTO Contains VALUES ('{}', '{}', '{}')".format(oid, items[i]['mid'], items[i]['amount'])
                db.session.execute(sql)
            except Exception as err:
                print("contains")
                return {"message": "error! change information error","state":False}
           
        response["message"]= True
        response['state']= True
    return response
        

if __name__=='__main__':
    app.run(host='0.0.0.0', port=8082, debug=True)