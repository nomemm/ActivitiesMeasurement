from utils.extjs import RpcRouter


class MainApiClass(object):
    """
    main class to be called
    """

    def hello(self,name, user):
        return({
            'msg':'Hello %s!' % name
        })

class Router(RpcRouter):
    """
    router itself, it is needed to link extjs with django
    """

    def __init__(self):
        self.url = 'main:router'

        self.actions = {
            'MainApi': MainApiClass()
        }
        self.enable_buffer = 50
