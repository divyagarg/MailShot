from flask import Flask


def create_app():
    app = Flask(__name__)
    from app.api_1_0 import api as api_1_0_blueprint

    app.register_blueprint(api_1_0_blueprint, url_prefix='/campaign/v1')
    return app


# @api.route('/test', methods=['GET'])
# @json
# def test():
# logger.info("Getting call for test function with request data %s", request.data)
# 	result = {"success": True}
# 	return result

