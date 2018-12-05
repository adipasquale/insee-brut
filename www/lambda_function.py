import json
from build import rebuild_all
from uploader import upload_files
import subprocess
from settings import BUILD_PATH

def lambda_handler(event, context):
    rebuild_all()
    upload_files()
    return {
        'statusCode': 201,
        'body': json.dumps('Hello from Lambda!')
    }

if __name__ == '__main__':
    print("wat")
    lambda_handler(None, None)