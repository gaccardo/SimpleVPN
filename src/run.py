from api.resources import user, certificate, profile, rule

from api.app import get_app

get_app().run(host='0.0.0.0', threaded=True)
