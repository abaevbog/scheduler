const remove = (z, bundle) => {
    z.console.log(bundle.inputData);
    const promise = z.request({
        url:'https://usx0yjoww7.execute-api.us-east-1.amazonaws.com/dev/delayer/delete',
        method: 'POST',
        body: bundle.inputData,
        headers: {
          'Authorization' : 'bmasters2020'
          }
        }
    )
    return promise.then(response => response.json)
  }  


  module.exports = {
    key: 'removeDelayer',
    noun: 'Rmove from Delayer ',
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
            key: 'delayer_db_internal_tag',
            required: true,
            label: 'delayer database internal tag of the entry that will be removed',
            dynamic: 'find_codes.id.name'
        }
      ],
    }
  }

  