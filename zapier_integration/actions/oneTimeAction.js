

const addRecordToDB = (z, bundle) => {
    z.console.log(bundle.inputData);
    const promise = z.request({
        url:'https://usx0yjoww7.execute-api.us-east-1.amazonaws.com/dev/add',
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
      description: 'Add entry to DB that should be triggered only once',
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
          key: 'reminders_db_internal_tag',
          required: true,
          label: 'Reminders database internal tag',
          choices: { 
            'vp-01' : 'VP-01 flow',
            'vp-02-01a' : 'VP-02-01a: wait for 4 weeks till precon',
          }
        },
        {
          key: 'reminders_db_internal_comment',
          required: true,
          label: 'Please add an internal comment to what this entry is.',
        },
        {
          key: 'next_action',
          required: true,
          label: 'Date of the next action. Format: YYYY-MM-DD HH:MM:SS.',
        },
        {
          key: 'type',
          required: true,
          label: 'Type of the action that should be taken.',
          choices: { 
            email : 'Email',
            text: 'Text',
            other: 'Other',
            email_and_text: "Email And Text"
          },
        },
      ],
    }
  }

  