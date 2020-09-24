
class TencentOss():
    def __init__(self):
        pass

    def auth(self, bucketName, endpointDomain, accessKeyId, accessKeySecret):
        self.bucketName = bucketName
        self.endpoint = endpointDomain

        self.region = re.search(r'\w+-\w+', self.endpoint)
        self.bucketDomain = 'https://%s.%s' % (self.bucketName, self.endpoint)

        self.secret_id = accessKeyId
        self.secret_key = accessKeySecret

        self.token = None  # 使用临时密钥需要传入 Token，默认为空，可不填
        self.scheme = 'https'  # 指定使用 http/https 协议来访问 COS，默认为 https，可不填

        self.proxies = {
            'http': '127.0.0.1:80',  # 替换为用户的 HTTP代理地址
            'https': '127.0.0.1:443'  # 替换为用户的 HTTPS代理地址
        }

        self.config = CosConfig(Region=self.region, SecretId=self.secret_id, SecretKey=self.secret_key,
                                Token=self.token,
                                Scheme=self.scheme, Endpoint=self.endpoint)
        self.client = CosS3Client(self.config)

    def create(self):
        # 创建存储桶
        response = self.client.create_bucket(
            Bucket=self.bucketName
        )
        return response

    def upload(self, source, destination):
        #### 文件流简单上传（不支持超过5G的文件，推荐使用下方高级上传接口）
        # 强烈建议您以二进制模式(binary mode)打开文件,否则可能会导致错误
        with open(source, 'rb') as fp:
            response = self.client.put_object(
                Bucket=self.bucketName,
                Body=fp,
                Key=destination,
                StorageClass='STANDARD',
                EnableMD5=False
            )
        # print(response['ETag'])
        remoteLink = 'https://' + urllib.parse.quote('%s.%s/%s' % (self.bucketName, self.endpoint, destination))
        return remoteLink

    def download(self, source, destination):
        #  获取文件到本地
        response = self.client.get_object(
            Bucket=self.bucketName,
            Key=source,
        )
        response['Body'].get_stream_to_file(destination)

    def delete(self, cloudFile):
        # cloudFile 表示删除OSS文件时需要指定包含文件后缀在内的完整路径，例如abc/efg/123.jpg。string 格式哦
        response = self.client.delete_object(
            Bucket=self.bucketName,
            Key=cloudFile
        )
