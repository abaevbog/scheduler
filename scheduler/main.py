from delayer.delayer import Delayer
from reminders.reminders import Reminders
from salesforce import Salesforce
import configparser
import sys

def main():
    print("STARTED")
    print(sys.argv)
    config = configparser.ConfigParser()
    config.read('scheduler.conf')
    operator_name = sys.argv[1]
    if operator_name == "delayer":
        print("DELAYER")
        operator = Delayer(config)
    elif operator_name == "reminder":
        print("REMINDER")
        operator = Reminders(config)
    else:
        raise Exception(f"Unknown operator {operator_name}")

    operator.update_records_before_trigger()
    operator.perform_trigger_actions()
    operator.update_records_after_trigger()

    operator.conn.close()
    print("Done")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
        sys.exit(1)
