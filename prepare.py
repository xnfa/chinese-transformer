from argparse import ArgumentParser
import boto3
import os, sys

BUCKET_NAME = 'deansel' # replace with your bucket name
s3 = boto3.resource('s3')

parser = ArgumentParser()
parser.add_argument("-i", "--input", dest="input",
                    help="hash of text source on S3")
parser.add_argument("-s", "--storage-dir", dest="STORAGE_DIR",
                    help="STORAGE_DIR")

STORAGE_DIR = parser.parse_args().STORAGE_DIR or '/storage/'
directory = parser.parse_args().input

try:
  os.makedirs(STORAGE_DIR + directory + '/test')
  os.makedirs(STORAGE_DIR + directory + '/train')
  os.makedirs(STORAGE_DIR + directory + '/valid')
except Exception as e:
  print(e)

s3.Bucket(BUCKET_NAME).download_file('source/' + directory + '/test.txt', STORAGE_DIR + directory + '/test/test.txt')
s3.Bucket(BUCKET_NAME).download_file('source/' + directory + '/train.txt', STORAGE_DIR + directory + '/train/train.txt')
s3.Bucket(BUCKET_NAME).download_file('source/' + directory + '/valid.txt', STORAGE_DIR + directory + '/valid/valid.txt')

print('Finshed prepare text')
