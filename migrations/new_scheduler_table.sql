SET timezone = 'America/New_York';

/*reminders settings*/
CREATE TYPE cutoff AS 
(
days_before_start  int,
freq_before int,
freq_after int
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
cutoff          cutoff          NOT NULL,
trigger_date_definition   trigger_date_definition,
indefinite boolean default false,
required_salesforce_fields VARCHAR(250)[] default array[]::varchar[250],
ID   SERIAL     PRIMARY KEY      NOT NULL,
created_at timestamp default (current_timestamp(0) at time zone 'America/New_York')
);

/*reminders table*/
CREATE TABLE DELAYER_V2
(
lead_id        VARCHAR(250)        NOT NULL,
project_name   VARCHAR(250)        NOT NULL,
tag            VARCHAR(250)        NOT NULL,
additional_info      TEXT                 ,
trigger_date_definition trigger_date_definition,
ID   SERIAL     PRIMARY KEY      NOT NULL,
created_at timestamp default (current_timestamp(0) at time zone 'America/New_York') 
);


CREATE TABLE salesforce_recs 
(
id VARCHAR(250) NOT NULL,
name VARCHAR(250),
satisfied VARCHAR(250)[] default array[]::varchar[250],
not_satisfied VARCHAR(250)[] default array[]::varchar[250] ,
status VARCHAR(250),
START_DATE timestamp
);

ALTER TABLE REMINDER ADD CONSTRAINT unique_entries_reminder UNIQUE (lead_id, project_name, tag);

ALTER TABLE DELAYER_V2 ADD CONSTRAINT unique_entries_delayer UNIQUE (lead_id, project_name, tag);