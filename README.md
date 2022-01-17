# Combining FastAPI with a Module listening for HTTP Requests

This program has two sections: the FastAPI *frontend*, and the module *backend*. The FastAPI waits for HTTP requests, and shares them with the *backend* through ZMQ sockets. The results are then shown back through FastAPI. 

This is only a proof of principle setup to show how such an architecture can be implemented. By no means it is fail-proof. 

## How to get started

The libraries required are:

- FastAPI (with uvicorn)
- PyZMQ

The **module_a.py** file has an example of a module that handles a request cycle. It is built on the **base_module.py**, which handles the cycle of get or put of an http request. 

The **start_experiment.py** file is the entry point for the backend. It loads the experiment, the configuration file, puts it in a state ready to start receiving messages. To start it the following command is enough:

```bash
python start_experiment.py
```

**The FastAPI** side is within the **main.py** file. It is based on the example of the official documentation. The relevant function is ``instrument_command``, which is just a proxy to the instrument messages. To start the server, we must run:

```bash
uvicorn main:app --reload
```

We can visit [http://localhost:8000/module_a/attributes](http://localhost:8000/module_a/attributes) to see the answer from the module itself. 

To stop the experiment one can just use CTRL+C. The **start_experiment** script will take care of gratiously stop listening on the ZMQ socket and close it. 

## For the Future
In this implementation, any crash would stop the process and there's no way of re-starting it. In case of deploying to an edge computer (or server) this would imply rebooting the system. To avoid this problem, checking a library such as [Supervisor](http://supervisord.org/) is crucial. 

Given that the system will be used in a low-risk setting (it is not a server exposed to thousands of requests per second), it is likely that a reverse-proxy like Nginx will not be necessary. Exposing directly uvicorn may be enough for most purposes. 

For the Python implementation itself, there's plenty of room for abstraction and to make the code more robuts. I have focused on dealing with some exceptions just to show how can this be done, but by no means this is complete or the best way of doing it. 

Introspection (i.e. checking which methods and attributes are available in an object) can simplify a lot the cycle of getting a request for a given instrument and routing it, etc. This level of abstraction, however, is very error prone and must be accompanied by extensive documentation. 