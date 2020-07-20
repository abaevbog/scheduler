

const addRecordToDB = (z, bundle) => {
    z.console.log(bundle.inputData);
    const promise = z.request({
        url:'https://usx0yjoww7.execute-api.us-east-1.amazonaws.com/dev/delayer/add',
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
    key: 'oneTimeAction',
    noun: 'Add Entry to Delay DB',
    display: {
      label: 'Single event to be tiggered in the future',
      description: 'Add entry to DB that will be triggered once in the future',
    },
    operation: {
      perform: addRecordToDB,
      inputFields: [
        {
          key: 'lead_id',
          required: true,
          label: 'ID of the lead',
        },
        {
          key: 'delayer_db_internal_tag',
          required: true,
          label: 'delayer database internal tag',
          choices: { 
            'vp-01-01c' : 'VP-01 flow',
            'vp-02-01c': 'VP-02-01c: catch start date webhook',
            'vp-02-01i': 'VP-02-01i send delayer',
            'vp-02-01g': 'VP-02-01g QCL and 2d invoice',
            'vp-02-01h': 'VP-02-01h 2d invoice to todoist and slack',
            'pm-03-01' : 'weekly reminders',
            'ycb-reminders' : 'Youcanbookme: send reminders before appointment'
          }
        },
        {
          key: 'delayer_db_internal_comment',
          required: true,
          label: 'Please add an internal comment to what this entry is.',
        },
        {
          key: 'trigger_date',
          required: true,
          label: 'Date of the next action. Format: YYYY-MM-DD HH:MM:SS.',
        },
        {
          key: 'additional_info',
          required: false,
          label: 'Optional additional info about the record',
        }
      ],
    }
  }

  