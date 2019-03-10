import smartcar
from flask import Flask, redirect, request, jsonify
from flask_cors import CORS
from twilio.twiml.messaging_response import MessagingResponse

import os

app = Flask(__name__)
CORS(app)

# global variable to save our access_token
access = None

client = smartcar.AuthClient(
    client_id='b6d2cfaf-2a34-435a-82af-b27d871ce3d5',
    client_secret='98238e90-c314-445f-b020-5f8480716c95',
    redirect_uri='http://localhost:8000/exchange',
    scope=['read_vehicle_info', 'control_security' , 'control_security:unlock', 'control_security:lock'],
    test_mode=False
)


@app.route('/login', methods=['GET'])
def login():
    auth_url = client.get_auth_url()
    return redirect(auth_url)


@app.route('/exchange', methods=['GET'])
def exchange():
    code = request.args.get('code')

    # access our global variable and store our access tokens
    global access
    # in a production app you'll want to store this in some kind of
    # persistent storage
    access = client.exchange_code(code)
    return '', 200

@app.route('/vehicle1', methods=['POST'])
def vehicle1():
    # access our global variable to retrieve our access tokens
    global access
    # the list of vehicle ids
    vehicle_ids = smartcar.get_vehicle_ids(
        access['access_token'])['vehicles']

    # instantiate the first vehicle in the vehicle id list
    vehicle = smartcar.Vehicle(vehicle_ids[0], access['access_token'])

    auth_url = '530a59a5.ngrok.io'

    info = vehicle.lock()
    print ("You may return to main page")

@app.route('/lockpage', methods=['GET'])
def lockpage(): 
        return '''
    <html>
        <body>
            <h2>Car locker</h2>
            <form action="/vehicle1" method="post">
                <button onclick="alert('You locked the car!')">Click to lock</button>
            </form>
        </body>
    </html>
    '''

@app.route('/vehicle', methods=['POST'])
def vehicle():
    # access our global variable to retrieve our access tokens
    global access
    # the list of vehicle ids
    vehicle_ids = smartcar.get_vehicle_ids(
        access['access_token'])['vehicles']

    # instantiate the first vehicle in the vehicle id list
    vehicle = smartcar.Vehicle(vehicle_ids[0], access['access_token'])

    auth_url = '2509bbe2.ngrok.io'

    info = vehicle.unlock()

    print ("You may exit")

@app.route('/unlockpage', methods=['GET'])
def unlockpage(): 
        return '''
    <html>
        <body>
            <h2>Car Unlocker</h2>
            <form action="/vehicle" method="post">
                <button onclick="alert('You have unlocked car!')">Click to unlock</button>
            </form>
        </body>
    </html>
'''

@app.route("/sms", methods=['GET', 'POST'])
def incoming_sms():
    """Send a dynamic reply to an incoming text message"""
    # Get the message the user sent our Twilio number
    body = request.values.get('Body', None)

    # Start our TwiML response
    resp = MessagingResponse()

    # Determine the right reply for this message
    print(body)
    
    if body == 'Hackru2019':
        global access
        vehicle_ids = smartcar.get_vehicle_ids(
        access['access_token'])['vehicles']

        # instantiate the first vehicle in the vehicle id list
        vehicle = smartcar.Vehicle(vehicle_ids[0], access['access_token'])

        vehicle.unlock()
        resp.message("Unlocked!")
        return str(resp)

    elif body != 'Hackru2019':
        vehicle_ids = smartcar.get_vehicle_ids(
        access['access_token'])['vehicles']

        # instantiate the first vehicle in the vehicle id list
        vehicle = smartcar.Vehicle(vehicle_ids[0], access['access_token'])

        vehicle.lock()
        resp.message("locked!")
        return str(resp)

if __name__ == '__main__':
    app.run(port=8000)



