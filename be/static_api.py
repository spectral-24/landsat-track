import falcon, json
import mimetypes
class StaticAPI:
    def on_get(self, req, resp, file):
        try:
            content_type = mimetypes.guess_type(file)[0]
            fd = open('./static/' + file, 'rb')
        except:
            resp.text = "Error opening the file"
            resp.status = 500
            return
            pass

        resp.content_type = content_type
        resp.text = fd.read()
        resp.status = falcon.HTTP_200
