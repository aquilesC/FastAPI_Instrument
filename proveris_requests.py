import requests

DEBUG = True


class ProverisRequests:
    @classmethod
    def put(self, url, payload):
        if DEBUG:
            np.save(payload, url)
        else:
            requests.put(url, payload)