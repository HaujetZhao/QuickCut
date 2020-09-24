
# 一个空的 oss 对象
class NoOss():
    def __init__(self):
        pass

    def auth(self, bucketName, endpointDomain, accessKeyId, accessKeySecret):
        pass

    def create(self):
        pass

    def upload(self, source, destination):
        pass

    def download(self, source, destination):
        pass

    def delete(self, cloudFile):
        pass
