class TuxMakeException(Exception):
    pass


class InvalidTarget(TuxMakeException):
    pass


class InvalidArchitecture(TuxMakeException):
    pass


class InvalidToolchain(TuxMakeException):
    pass
