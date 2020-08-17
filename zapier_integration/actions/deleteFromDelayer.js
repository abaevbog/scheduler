const remove = (z, bundle) => {
    z.console.log(bundle.inputData);
    const promise = z.request({
        url:'https://9b8pw4g950.execute-api.us-east-1.amazonaws.com/v2/delete',
        method: 'POST',
        body: bundle.inputData,
        params:{
          'operator': 'delayer'
        },
        headers: {
          'Authorization' : 'bmasters2020'
          }
        }
    )
    return promise.then(response => response.json)
  }  


  module.exports = {
    key: 'deleteFromDelayer',
    noun: 'Remove from Delayer ',
    display: {
      label: 'Remove from delayer',
      description: 'Delete existing entry in delayer database',
    },
    operation: {
      perform: remove,
      inputFields: [
        {
          key: 'lead_id',
          required: true,
          label: 'Lead id of the entry that will be removed',
        },
        {
            key: 'tag',
            required: true,
            label: 'delayer database internal tag of the entry that will be removed',
            dynamic: 'find_codes.id.name'
        }
      ],
    }
  }

  