import json

def getPathAndRowFromFolder(folder):
    relevant = folder.split('_')[2]
    return map(int, [relevant[0:3], relevant[3:]])

def copy_object(a,b):
    print(a,b)

def process_handler(eventStr, handler):
    event = json.loads(eventStr)
    paths = event['Records'][0]['s3']['object']['key'].split('/')

    folder_name = paths[-2]
    [path, row] = getPathAndRowFromFolder(folder_name)

    # Check the database fr if there are records for this path
    # the hit should have already happened

    # db_row = get_db_row_with_path_and_row(path, row)
    handler(path, row, paths, folder_name)
    db_row = True
    if (db_row):
        prefix = '/'.join(paths[:-1]) + '/' + folder_name
        for suffix in ['_MTL.json', '_ST_stac.json', '_thumb_large.jpeg']:
            copy_object(prefix + suffix, folder_name + suffix)
            break
        # notify_user_about_data(db_row, folder_name)