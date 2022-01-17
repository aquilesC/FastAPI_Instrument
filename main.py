from fastapi import FastAPI
import zmq


app = FastAPI()

# To communicate with the instrument, first the 'experiment.py' file has to run

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect('tcp://localhost:5555')


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/{module}/{command}")
def instrument_command(module, command):
    socket.send_json({module: command})
    message = socket.recv()
    return {"message": command, "value": message}