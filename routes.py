from translator import IndicTranslator


def add_routes_to_resource(_api):
    _api.add_resource(IndicTranslator, '/get_message', strict_slashes=False)
