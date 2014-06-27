-- Target table
DROP TABLE IF EXISTS messages CASCADE;

create table messages (
 id serial primary key,
 date timestamp without time zone,
 carrier text,
 message text
);

-- Staging table; will gather updates until processed
CREATE OR REPLACE FUNCTION table_message_notify() RETURNS trigger AS $$                                                                                                                          
DECLARE                                                                                                                                                                                       
BEGIN                                                                                                                                                                                         
  PERFORM pg_notify('table_messages_notifier',CAST(NEW.id AS text));
   RETURN NEW;
  END;
$$ LANGUAGE plpgsql;
                 
CREATE TRIGGER object_post_insert_notify AFTER insert ON messages FOR EACH ROW EXECUTE PROCEDURE table_message_notify();
