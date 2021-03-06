#Murali
from flask import Flask
from flask import render_template,jsonify,request
import requests
# from models import *
from engine import *
import random
app = Flask(__name__)
app.secret_key = '12345'

@app.route('/')
def hello_world():
    return render_template('home-SELECT.html', data=[{'name':'Recruiter'},{'name':'HR-Manager'},{'name':'LOB-Head'}])

@app.route('/test', methods=['GET', 'POST'])
def test():
    select = request.form.get('comp_select')
    print(select);
    if select == "Recruiter":
        return(render_template('Recruiter.html', data1='Recruiter'))
    elif select == "HR-Manager":
        return(render_template('HR-Manager.html', data1='HR-Manager'))
    elif select == "LOB-Head":
        return(render_template('LOB-Head.html', data1='LOB-Head'))
	
	
get_random_response = lambda intent:random.choice(intent_response_dict[intent])


@app.route('/chat',methods=["POST"])
def chat():
    try:
        user_message = request.form["text"]
        response = requests.get("http://localhost:5000/parse",params={"q":user_message})
        response = response.json()
        entities = response.get("entities")
        topresponse = response["topScoringIntent"]
        intent = topresponse.get("intent")
        print("Intent {}, Entities {}".format(intent,entities))
        if intent == "event-name":
            response_text = hr_info(entities)
        elif intent == "event-name":
            response_text = req_query(entities)
        else:
            response_text = get_random_response(intent)
        return jsonify({"status":"success","response":response_text})
    except Exception as e:
        print(e)
        return jsonify({"status":"success","response":"Apologies! I am yet to be trained to respond to this query..."})


app.config["DEBUG"] = True
if __name__ == "__main__":
    app.run(host="DESKTOP-NJ1L93T",port=8080)
