PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE api (
                                    id integer primary key autoincrement,
                                    name text, 
                                    provider text, 
                                    appKey text, 
                                    language text, 
                                    accessKeyId text, 
                                    accessKeySecret text
                                    );
COMMIT;
