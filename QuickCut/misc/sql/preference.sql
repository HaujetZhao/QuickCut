PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE preference (
                                            id integer primary key autoincrement,
                                            item text,
                                            value text
                                            );
INSERT INTO preference VALUES(1,'hideToTrayWhenHitCloseButton','False');
INSERT INTO preference VALUES(2,'language','中文');
COMMIT;
