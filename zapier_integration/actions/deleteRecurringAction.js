const remove = (z, bundle) => {
    z.console.log(bundle.inputData);
    const promise = z.request({
        url:'https://usx0yjoww7.execute-api.us-east-1.amazonaws.com/dev/scheduler/delete',
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
    key: 'removeScheduler',
    noun: 'Rmove recurring action',
    display: {
      label: 'Remove recurring action',
      description: 'Delete existing entry in scheduler database',
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
            key: 'scheduler_db_internal_tag',
            required: true,
            label: 'scheduler database internal tag of the entry that will be removed',
            dynamic: 'find_codes.id.name'
        }
      ],
    }
  }