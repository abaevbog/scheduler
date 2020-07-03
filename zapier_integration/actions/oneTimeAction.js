

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
    noun: 'oneTimeAction',
    display: {
      label: 'Action that should happen in the future once',
      description: 'Action that should happen in the future once',
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
          key: 'lead_status',
          required: true,
          label: 'Status of the lead.',
          choices: { 
            'vp-01' : 'VP-01 flow'
          },
        },
        {
          key: 'next_action',
          required: true,
          label: 'Date of the next action. Format: YYYY-MM-DD HH:MM:SS.',
        },
        {
          key: 'comment',
          required: true,
          label: 'Please add a comment to what this entry is. Should be informative as it can be useful during troubleshooting.',
        },
        {
          key: 'type',
          required: true,
          label: 'Type of the action that should be taken.',
          choices: { 
            email : 'Email',
            text: 'Text',
            other: 'Other'
          },
        },
      ],
    }
  }

  