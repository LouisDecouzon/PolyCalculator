import pika, redis
import os, sys
redis_client = redis.Redis(host='localhost', port=6379, db=0)
def main():
    
    try:
        redis_client.ping()
        print("Connexion réussie à Redis !")
    except redis.ConnectionError:
        print("Échec de connexion à Redis.")
    #redis_client.set('calculus',calculus)
    pika_queue = pika.BlockingConnection(pika.ConnectionParameters('localhost',5672))
    channel = pika_queue.channel()
    channel.queue_declare(queue='hello')
    def callback(ch, method, properties, body):

        send_to_redis(body)
        print(f"[O] Sent {str(body)} to redis")
    channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)
    print('[*] Waiting for messages.')
    channel.start_consuming()

def send_to_redis(calculus:str):
    calculus=str(calculus)
    if calculus.startswith("b'") and calculus.endswith("'"):
        calculus=calculus[2:-1]
    elif calculus.startswith('b"') and calculus.endswith('"'):
        calculus = calculus[2:-1]
    redis_client.lpush("results",f"{compute(calculus)}")


def compute(calculus:str):
    calculus = calculus.strip()
    
    operateur = None
    for op in ['+', '-', '*', '/']:
        if op in calculus:
            operateur = op
            break
    
    if operateur is None:
        if calculus=="":
            return 0
        raise ValueError("Operator not found")
    try:
        a, b = map(float, calculus.split(operateur))
    except ValueError:
        raise ValueError("Invalid format")
    
    if operateur == '+':
        return a + b
    elif operateur == '-':
        return a - b
    elif operateur == '*':
        return a * b
    elif operateur == '/':
        if b == 0:
            raise ZeroDivisionError("Division by zero, Ouch!")
        return a / b

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)