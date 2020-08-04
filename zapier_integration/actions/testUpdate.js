const listZapCodes = (z, bundle) => {
    z.console.log(z.inputData)
    const promise = z.request(
      'https://usx0yjoww7.execute-api.us-east-1.amazonaws.com/dev/codes'
    )
    return promise.then(response => response.json)
  }
  
  
  
  const uuupppdddaaatte = (z, bundle) => {
      z.console.log(bundle.inputData);
      const promise = z.request({
          url:'https://usx0yjoww7.execute-api.us-east-1.amazonaws.com/dev/delayer/update',
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
      key: 'uuupppdddaaatteDelayer',
      noun: 'uuupppdddaaatte Delayer ',
      display: {
        label: 'uuupppdddaaatte delayer',
        description: 'uuupppdddaaatte existing entry in delayer database',
      },
      operation: {
        perform: uuupppdddaaatte,
        inputFields: [
          {
            key: 'lead_id',
            required: true,
            label: 'Lead id of the entry that will be uuupppdddaaatted',
          },
          {
              key: 'delayer_db_internal_tag',
              required: true,
              label: 'delayer database internal tag of the entry that will be uuupppdddaaatted',
              dynamic: 'find_codes.id.name'
          },
          {
            key: 'additional_info',
            required: true,
            label: 'Value of additional_info field of the entry in the database that will be uuupppdddaaatted',
          },
          {
              key: 'trigger_date',
              required: true,
              label: 'New trigger date the entry in the delayer. Format: YYYY-MM-DD HH:MM:SS. ',
            }
        ],
      }
    }
  
    