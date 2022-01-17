from base_module import BaseModule


class ModuleA(BaseModule):
    def __init__(self, ip, port, name=None):
        super().__init__(ip, port)

        self.name = name

    def get_attributes(self):
        endpoint = 'attributes'
        attributes = self.get(endpoint)
        return attributes

    def get_parameters(self):
        endpoint = 'parameters'
        parameters = self.get(endpoint)
        return parameters

    def __str__(self):
        return f"ModuleA on {self.ip}:{self.port}"