import zmq

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect('tcp://localhost:5555')

socket.send_string("idn")
message = socket.recv()
print(message)

socket.send_string("measure_temp")
message = socket.recv()
print(message)


