from core.update import UpdateOS


class BasicTask(UpdateOS):

    def __init__(self):
        super(BasicTask, self).__init__()

    def install(self):
        raise NotImplementedError

    def configure(self):
        raise NotImplementedError
