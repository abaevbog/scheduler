SET timezone = 'America/New_York';

/*reminders settings*/
CREATE TYPE settings AS 
(
frequency_cutoff timestamp,
freq_before_cutoff int,
freq_after_cutoff int
);

CREATE TYPE trigger_date_definition AS
(
days_before_start int,
next_date timestamp
);


/*reminders table*/
CREATE TABLE REMINDER
(
lead_id        VARCHAR(250)        NOT NULL,
project_name   VARCHAR(250)        NOT NULL,
tag            VARCHAR(250)        NOT NULL,
additional_info      TEXT                 ,
settings        settings          NOT NULL,
trigger_date_definition   trigger_date_definition,
required_salesforce_fields VARCHAR(250)[] default array[]::varchar[250],
ID   SERIAL     PRIMARY KEY      NOT NULL,
created_at timestamp default current_timestamp(0)
);

/*reminders table*/
CREATE TABLE DELAYER
(
lead_id        VARCHAR(250)        NOT NULL,
project_name   VARCHAR(250)        NOT NULL,
tag            VARCHAR(250)        NOT NULL,
additional_info      TEXT                 ,
trigger_date_definition trigger_date_definition,
ID   SERIAL     PRIMARY KEY      NOT NULL,
created_at timestamp default current_timestamp(0)
);


CREATE TABLE salesforce_recs 
(
id VARCHAR(250) NOT NULL,
name VARCHAR(250),
satisfied VARCHAR(250)[] default array[]::varchar[250],
not_satisfied VARCHAR(250)[] default array[]::varchar[250] ,
status VARCHAR(250),
START_DATE timestamp,
);

ALTER TABLE REMINDER ADD CONSTRAINT unique_entries UNIQUE (lead_id, project_name, tag);

ALTER TABLE DELAYER ADD CONSTRAINT unique_entries UNIQUE (lead_id, project_name, tag);