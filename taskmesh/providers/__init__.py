class Provider:
    def run(self, topic, func, config):
        raise NotImplementedError("This method should be implemented by the subclass")
