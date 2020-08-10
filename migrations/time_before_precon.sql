ALTER TABLE scheduler
ADD COLUMN days_before_precon_or_predemo INT;

ALTER TABLE delayer
ADD COLUMN days_before_precon_or_predemo INT;

/*ALTER TABLE scheduler
ADD COLUMN precon_or_predemo TEXT;

ALTER TABLE delayer
ADD COLUMN precon_or_predemo TEXT;*/

ALTER TABLE scheduler
ADD COLUMN wait_for_precon_or_predemo TEXT;

ALTER TABLE delayer
ADD COLUMN wait_for_precon_or_predemo TEXT;

ALTER TABLE scheduler
ADD COLUMN precon_or_predemo_date timestamp;

ALTER TABLE delayer
ADD COLUMN precon_or_predemo_date timestamp;