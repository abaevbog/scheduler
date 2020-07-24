ALTER TABLE scheduler ADD COLUMN on_hold BOOLEAN default FALSE;
ALTER TABLE delayer ADD COLUMN on_hold BOOLEAN default FALSE;

SET timezone = 'America/New_York';

ALTER TABLE scheduler 
ADD COLUMN created_at timestamp default current_timestamp(0);

ALTER TABLE delayer
ADD COLUMN created_at timestamp default current_timestamp(0);