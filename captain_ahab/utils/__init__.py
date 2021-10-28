

def generate_default_config():
    pass


class Singleton(type):
    def __init__(cls, name, bases, d):
        super().__init__(name, bases, d)
        cls.instance = None

    def __call__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__call__(*args, **kwargs)
        return cls.instance


__all__ = ['generate_default_config', 'Singleton']
