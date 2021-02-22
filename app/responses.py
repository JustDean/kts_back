from aiohttp import web


def json_response(status=200, text_status="ok", data=None):
    return web.json_response(status=status, data={"data": data, "status": text_status})


def error_json_response(status=400, text_status="ok", message="Bad request", data=None):
    return web.json_response(status=status, data={"data": data, "status": text_status, "message": message})
