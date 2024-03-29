import paho.mqtt.client as paho
import time
import ssl
import random
import string

from server import process_message, post_or_update_entity, create_subscription, get_historical_data


import json

# Function to generate a random ID
def generate_random_id(length):
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for i in range(length))

# Subscriber
def on_connect_subscriber(client, userdata, flags, rc):
    topic = "/fhtw/368415464/9hids/we2j332"
    client.subscribe(topic, 0)

def on_message_subscriber(client, userdata, message):
    message = json.loads(message.payload.decode("utf-8"))
    ngsi_entity = process_message(message)
    post_or_update_entity(ngsi_entity)
    

def main():

    #get_historical_data("urn:ngsi-v2:Sensor:1")
    create_subscription()
    
    uid_subscriber = generate_random_id(16)
    client_subscriber = paho.Client(uid_subscriber)
    client_subscriber.on_connect = on_connect_subscriber
    client_subscriber.on_message = on_message_subscriber

    broker = "test.mosquitto.org"

    print("Connecting to broker for subscribing...")
    client_subscriber.tls_set(cert_reqs=ssl.CERT_NONE)
    client_subscriber.tls_insecure_set(True)
    client_subscriber.connect(broker, 8883, 60)
    client_subscriber.loop_start()
    print("Connected for subscribing - loop started")

    time.sleep(60)

    # Stopping subscriber loop
    client_subscriber.loop_stop()
    client_subscriber.disconnect()
    print("Disconnected for subscribing.")


if __name__ == "__main__":
    main()

   