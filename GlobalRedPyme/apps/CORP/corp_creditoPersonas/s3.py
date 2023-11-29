# Importar boto3
import boto3
import environ
# environ init
env = environ.Env()
environ.Env.read_env()  # LEE ARCHIVO .ENV

session = boto3.Session(
    aws_access_key_id=env.str('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=env.str('AWS_SECRET_ACCESS_KEY')
)

s3 = session.resource('s3')
s3bkt = s3.Bucket(env.str('AWS_STORAGE_BUCKET_NAME'))
s3bktreplay = s3.Bucket(env.str('AWS_STORAGE_BUCKET_NAME_BIGPUNTOS'))

def replicate(key):
    # for s3_file in s3bkt.objects.all():
    copy_source = {"Bucket": env.str('AWS_STORAGE_BUCKET_NAME'), "Key": key}

        # print(copy_source)
        # print(s3_file.key)
    s3bktreplay.copy(copy_source, key)