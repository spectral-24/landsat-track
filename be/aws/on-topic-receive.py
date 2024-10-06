import json

events = '''
{  
   "Records":[  
      {  
         "eventVersion":"2.2",
         "eventSource":"aws:s3",
         "awsRegion":"us-west-2",
         "eventTime":"The time, in ISO-8601 format, for example, 1970-01-01T00:00:00.000Z, when Amazon S3 finished processing the request",
         "eventName":"event-type",
         "userIdentity":{  
            "principalId":"Amazon-customer-ID-of-the-user-who-caused-the-event"
         },
         "requestParameters":{  
            "sourceIPAddress":"ip-address-where-request-came-from"
         },
         "responseElements":{  
            "x-amz-request-id":"Amazon S3 generated request ID",
            "x-amz-id-2":"Amazon S3 host that processed the request"
         },
         "s3":{  
            "s3SchemaVersion":"1.0",
            "configurationId":"ID found in the bucket notification configuration",
            "bucket":{  
               "name":"amzn-s3-demo-bucket",
               "ownerIdentity":{  
                  "principalId":"Amazon-customer-ID-of-the-bucket-owner"
               },
               "arn":"bucket-ARN"
            },
            "object":{  
               "key":"collection02/level-2/standard/oli-tirs/2024/010/009/LC08_L2SP_010009_20240806_20240814_02_T2/LC08_L2SP_010009_20240806_20240814_02_T2/index.html",
               "size":"object-size in bytes",
               "eTag":"object eTag",
               "versionId":"object version if bucket is versioning-enabled, otherwise null",
               "sequencer": "a string representation of a hexadecimal value used to determine event sequence, only used with PUTs and DELETEs"
            }
         },
         "glacierEventData": {
            "restoreEventData": {
               "lifecycleRestorationExpiryTime": "The time, in ISO-8601 format, for example, 1970-01-01T00:00:00.000Z, of Restore Expiry",
               "lifecycleRestoreStorageClass": "Source storage class for restore"
            }
         }
      }
   ]
}
'''
def getPathAndRowFromFolder(folder):
    relevant = folder.split('_')[2]
    return map(int, [relevant[0:3], relevant[3:]])

def copy_object(a,b):
    print(a,b)

def handler(eventStr):
    event = json.loads(eventStr)
    paths = event['Records'][0]['s3']['object']['key'].split('/')

    folder_name = paths[-2]
    [path, row] = getPathAndRowFromFolder(folder_name)

    # Check the database fr if there are records for this path
    # the hit should have already happened

    # db_row = get_db_row_with_path_and_row(path, row)
    db_row = True
    if (db_row):
        prefix = '/'.join(paths[:-1]) + '/' + folder_name
        for suffix in ['_MTL.json', '_ST_stac.json', '_thumb_large.jpeg']:
            copy_object(prefix + suffix, folder_name + suffix)
            break
        # notify_user_about_data(db_row, folder_name)

handler(events)