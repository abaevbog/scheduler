import salesforce

s = salesforce.Salesforce(token = '00Df40000025Uc7!AQoAQNutoILJzShsJ_TAfZIhdFxGU7fa2gbGCCyyPVBaZ87azCIn4g6wblXnq24Yw9sZx0NNsGAambNiqqgn2oTp_SoDvG2H')
token = s.authenticate()
print(token)
fields  = s.get_object_fields()

print(s.query(['00Qf400000OV4zKEAT'],fields))