#Le back en python
#Réceptionne la demande de calcul, la formate, calcule le résultat, 
#l'envoie avec le calcul à la BDD puis Narnia puis
#le back redemande le résultat et l'envoie au front

from flask import Flask, render_template, request
import json
import pika, sys, os, redis

app = Flask(__name__)
pika_queue = pika.BlockingConnection(pika.ConnectionParameters('localhost',5672))
channel = pika_queue.channel()    
channel.queue_declare(queue='hello')
redis_client = redis.Redis(host='localhost', port=6379, db=0)
try:
    redis_client.ping()
    print("Connexion réussie à Redis !")
except redis.ConnectionError:
        print("Échec de connexion à Redis.")

    



@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route("/calculus", methods=['POST'])
def process():
    data=request.get_json()
    calculus=data.get('calculus','')
    print(calculus)
    channel.basic_publish(exchange='', routing_key='hello', body=calculus)
    print("calculus sent to consumer")
    result = str(redis_client.lpop("results"))
    print("Result sent to front : ", result)

    return render_template("index.html",result=result)



if __name__ == '__main__':
    try:
        app.run(debug=True, host='0.0.0.0',port=5000)
    except KeyboardInterrupt:
        pika_queue.close()
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)