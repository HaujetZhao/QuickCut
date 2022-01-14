PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE oss (
                                    id integer primary key autoincrement,
                                    provider text, 
                                    endPoint text, 
                                    bucketName text, 
                                    bucketDomain text,
                                    accessKeyId text, 
                                    accessKeySecret text);
COMMIT;
