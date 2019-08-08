from argparse import ArgumentParser
import boto3
from botocore.exceptions import NoCredentialsError

BUCKET_NAME = 'deansel'

parser = ArgumentParser()
parser.add_argument("-i", "--input", dest="input",
                    help="hash of text source on S3")
parser.add_argument("-s", "--storage-dir", dest="STORAGE_DIR",
                    help="STORAGE_DIR")
parser.add_argument("-key", "--access-key", dest="ACCESS_KEY",
                    help="ACCESS_KEY")
parser.add_argument("-secret", "--secret-sccess-key", dest="SECRET_KEY",
                    help="SECRET_KEY")

ACCESS_KEY = parser.parse_args().ACCESS_KEY
SECRET_KEY = parser.parse_args().SECRET_KEY
STORAGE_DIR = parser.parse_args().STORAGE_DIR or '/storage/'
directory = parser.parse_args().input

s3 = boto3.client(
  's3',
  aws_access_key_id=ACCESS_KEY,
  aws_secret_access_key=SECRET_KEY
)

try:
    s3.upload_file(STORAGE_DIR + directory + '/dist/params.json', BUCKET_NAME, 'model/' + directory + '/params.json')
    s3.upload_file(STORAGE_DIR + directory + '/dist/model.pt', BUCKET_NAME, 'model/' + directory + '/model.pt')
    s3.upload_file(STORAGE_DIR + directory + '/dist/sp.model', BUCKET_NAME, 'model/' + directory + '/sp.model')
    print("Upload Successful")
except FileNotFoundError:
    print("The file was not found")
except NoCredentialsError:
    print("Credentials not available")