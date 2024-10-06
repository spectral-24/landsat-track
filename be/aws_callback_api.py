import falcon, json
import mimetypes
from image_fetching.sr_fetch import copy_object
from datetime import datetime
def getPathAndRowFromFolder(folder):
    relevant = folder.split('_')[2]
    return map(int, [relevant[0:3], relevant[3:]])

class AWSCallbackAPI:
    def __init__(self, dbcurs):
        self.dbcurs = dbcurs
    # We received a message in the queue from the lambda, from the USGS topic
    # As lambda just forwards, this should have the structure outlined in
    # https://docs.aws.amazon.com/AmazonS3/latest/userguide/notification-content-structure.html
    def on_post(self, req, resp):
        event = req.get_media()
        
        paths = event['Records'][0]['s3']['object']['key'].split('/')

        folder_name = paths[-2]
        [path, row] = getPathAndRowFromFolder(folder_name)

        resp.text = json.dumps([path, row, folder_name])
        resp.status = falcon.HTTP_200

        # Check the database for if there are records for this path
        # the hit should have already happened


        dbrows = self.dbcurs.execute(
            "SELECT email, phone, lat, lon FROM registrations WHERE path='{}' and row='{}' and datetime(hit) < datetime('{}')".format(path, row, datetime.now())
        ).fetchall()

        if(len(dbrows) > 0):
            prefix = '/'.join(paths[:-2]) + '/' + folder_name
            for suffix in ['_MTL.json', '_ST_stac.json', '_thumb_large.jpeg']:
                copy_object(prefix + suffix, folder_name + suffix)
        else:
            print('there were no entries')

        for dbrow in dbrows:
            [email, phone, lat, lon] = dbrow
            notify_user_about_data(email, phone, folder_name, lat, lon)