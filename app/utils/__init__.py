from .singleton import Singleton, SingletonThreadSafe  # noqa F401


def get(obj, *keys, **kwargs):
    try:
        value = obj[keys[0]]

        for key in keys[1:]:
            value = value[key]
    except (KeyError, IndexError, TypeError):
        return kwargs.get('default', None)

    return value
