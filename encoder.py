from connexion.apps.flask_app import FlaskJSONEncoder
import six

from models.base_model_ import Model


class JSONEncoder(FlaskJSONEncoder):
    """Default JSON encoder from the openapi generator.

    You can return any Model to the connexion server and it will be converted
    to JSON automatically.
    """
    include_nulls = False

    def default(self, o):
        if isinstance(o, Model):
            dikt = {}
            for attr, _ in six.iteritems(o.openapi_types):
                value = getattr(o, attr)
                if value is None and not self.include_nulls:
                    continue
                attr = o.attribute_map[attr]
                dikt[attr] = value
            return dikt
        return FlaskJSONEncoder.default(self, o)
