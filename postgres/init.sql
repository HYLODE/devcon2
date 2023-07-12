-- init.sql

DROP TABLE IF EXISTS names;
-- Create table
CREATE TABLE ids (
    unid INT PRIMARY KEY,
    messagedatetime TIMESTAMP,
    messagetype VARCHAR(16),
    senderapplication VARCHAR(180)
);

-- Copy data from CSV file
COPY ids(unid, messagedatetime,messagetype, senderapplication) 
FROM '/data/mock.csv' 
DELIMITER ',' 
CSV HEADER;

DROP TABLE IF EXISTS mytable;
CREATE TABLE mytable (
    name            varchar(80),
    pet             varchar(80)
);

INSERT INTO mytable VALUES ('Mary', 'dog'), ('John', 'cat'), ('Robert', 'bird');

