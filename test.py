import salesforce

s = salesforce.Salesforce(token = '00Df40000025Uc7!AQoAQFo7EwteUV_42RTkPQKJnZOMNJ7Hwk7OwLyhc84I6QgObgHtWl_nCb1wIlmPwqblSmkbgmUgZNw1iZikRVXbcBxBoTip')
token = s.authenticate()
#print(token)
checkbox_fields, date_fields  = s.get_object_fields()
s.get_salesforce_records(['00Qf400000OV4zKEAT'],list(set(checkbox_fields)) )
s.write_checkbox_records_to_s3()