

const update = (z, bundle) => {
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
    key: 'updateDelayer',
    noun: 'Update Delayer ',
    display: {
      label: 'Update delayer',
      description: 'Update existing entry in delayer database',
    },
    operation: {
      perform: update,
      inputFields: [
        {
          key: 'lead_id',
          required: true,
          label: 'Lead id of the entry that will be updated',
        },
        {
            key: 'delayer_db_internal_tag',
            required: true,
            label: 'delayer database internal tag of the entry that will be updated',
            choices: { 
              'vp-01-01c' : 'VP-01 flow',
              'vp-02-01c': 'VP-02-01c: catch start date webhook',
              'vp-02-01i': 'VP-02-01i send delayer',
              'vp-02-01g': 'VP-02-01g QCL and 2d invoice',
              'vp-02-01h': 'VP-02-01h 2d invoice to todoist and slack',
              'pm-03-01' : 'weekly reminders',
              'ycb-reminders' : 'Youcanbookme: communication with the client',
              'pm-05-03' : 'Ask PM and QCL if toilet needs removal',
              'pm-05-02' : 'Ask PM and QCL if toilet needs to be ordered'
            }
        },
        {
          key: 'additional_info',
          required: true,
          label: 'Value of additional_info field of the entry in the database that will be updated',
        },
        {
            key: 'trigger_date',
            required: true,
            label: 'New trigger date the entry in the delayer. Format: YYYY-MM-DD HH:MM:SS. ',
          }
      ],
    }
  }

  