# Combining FastAPI with an instrument

This program has two sections: the FastAPI backend, and the instrument backend. They communicate with each other via ZMQ sockets. 

This is only a proof of principle setup to show how such an architecture can be implemented. By no means it is fail-proof. 

## How to get started

The libraries required are:

- FastAPI (with uvicorn)
- PyZMQ

The **instrument.py** file has an example of an instrument that takes care of opening a socket for a REQ/REP cycle. This is done by triggering a method: ``wait_for_messages`` which is an infinite loop. 

The **experiment.py** file is the entry point. It loads the instrument and puts it in a state ready to start receiving messages. To start it the following command is enough:

```bash
python experiment.py
```

**The FastAPI** side is within the **main.py** file. It is based on the example of the official documentation. The relevant function is ``instrument_command``, which is just a proxy to the instrument messages. To start the server, we must run:

```bash
uvicorn main:app --reload
```

We can visit [http://localhost:8000/instrument/idn](http://localhost:8000/instrument/idn) to see the answer from the instrument itself. 

**Known caveats:** 

The ``wait_for_messages`` method is an infinite loop that has no way of being stopped besides stopping the program. 

In this current implementation, it would not be possible to have one than more instrument. To expand on this idea, there should be another layer taking care of creating the socket and some routing. 

## For the Future
In this implementation, any crash would stop the process and there's no way of re-starting it. In case of deploying to an edge computer (or server) this would imply rebooting the system. To avoid this problem, checking a library such as [Supervisor](http://supervisord.org/) is crucial. 

Given that the system will be used in a low-risk setting (it is not a server exposed to thousands of requests per second), it is likely that a reverse-proxy like Nginx will not be necessary. Exposing directly uvicorn may be enough for most purposes. 