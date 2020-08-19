from delayer.delayer import Delayer
from reminders.reminders import Reminders
from salesforce import Salesforce
import configparser
import sys

def main():
    config = configparser.ConfigParser()
    config.read('scheduler.conf')
    operator_name = sys.argv[1]
    if operator_name == "delayer":
        operator = Delayer(config)
    elif operator_name == "reminder":
        operator = Reminders(config)
    else:
        raise Exception(f"Unknown operator {operator_name}")
    operator.truncate_salesforce_records()
    operator.get_salesforce_data()
    operator.update_records_before_trigger()
    operator.perform_trigger_actions()
    operator.update_records_after_trigger()

    operator.conn.close()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Uncaught exception in {sys.argv[1]}: ", e)
        sys.exit(1)
