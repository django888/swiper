
from qiniu import Auth, put_file, etag
from common.config import *


def upload(file_name,file_path):
    #需要填写你的 Access Key 和 Secret Key
    # access_key = 'Access_Key'
    # secret_key = 'Secret_Key'

    #构建鉴权对象
    qn_auth = Auth(QN_ACCESS_KEY, QN_SECRET_KEY)

    #要上传的空间
    #上传后保存的文件名
    # key = 'my-python-logo.png'
    #
    #生成上传 Token，可以指定过期时间等
    token = qn_auth.upload_token(QN_BUCKET_NAME, file_name, 3600)

    #要上传文件的本地路径
    # localfile = './sync/bbb.jpg'

    ret, info = put_file(token, file_name, file_path)
    return ret,info
    # print(info)
    # assert ret['key'] == key
    # assert ret['hash'] == etag(localfile)
