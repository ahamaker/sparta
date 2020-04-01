from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

from pymongo import MongoClient             # pymongo를 import하기
client = MongoClient('localhost', 27017)    # mongo는 27017 포트로 돌아갑니다.
db = client.dbsparta                        # 'dbsparta'라는 이름의 db를 만듭니다.

# HTML을 주는 부분
@app.route('/')
def home():
    return render_template('product.html')

# API 역할을 하는 부분
@app.route('/order_list', methods=['POST'])
def write_order_info():
    # 1. 클라이언트가 준 orderer, amount, address, phone 가져오기.
    orderer_receive = request.form['orderer_give']
    amount_receive = request.form['amount_give']
    address_receive = request.form['address_give']
    phone_receive = request.form['phone_give']

    # 2. DB에 삽입할 order_info 만들기
    order_info = {
        'orderer': orderer_receive,
        'amount': amount_receive,
        'address': address_receive,
        'phone': phone_receive
    }

    # 3. DB collection 'order_list'에 order_info 저장하기
    db.order_list.insert_one(order_info)

    # 4. 성공 여부 & 성공 메시지 반환하기
    return jsonify({'result': 'success', 'msg': '주문이 성공적으로 접수되었습니다.'})


@app.route('/order_list', methods=['GET'])
def read_order_info():
    # 1. DB에서 주문자 정보 정보 모두 가져오기
    order_list = list(db.order_list.find({}, {'_id': 0}))
    # 2. 성공 여부 & 주문자 정보 반환하기
    return jsonify({'result': 'success', 'order_list': order_list})


if __name__ == '__main__':
    app.run('127.0.0.1', port=5000, debug=True)
