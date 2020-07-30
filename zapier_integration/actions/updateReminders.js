

const update = (z, bundle) => {
    z.console.log(bundle.inputData);
    const promise = z.request({
        url:'https://usx0yjoww7.execute-api.us-east-1.amazonaws.com/dev/scheduler/update',
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
    key: 'updateReminder',
    noun: 'Update reminder ',
    display: {
      label: 'Update reminder',
      description: 'Update existing reminder in reminders database',
    },
    operation: {
      perform: update,
      inputFields: [
        {
          key: 'lead_id',
          required: true,
          label: 'ID of the lead',
        },
        {
            key: 'next_action',
            required: false,
            label: 'Optionally, update the date of the next action. Format: YYYY-MM-DD HH:MM:SS. ',
          },
          {
              key: 'event_date',
              required: true,
              label: 'Update date of the key event after which the action is no longer repeated regardless of salesforce fields. Format: YYYY-MM-DD HH:MM:SS.',
          },
          {
              key: 'cutoff',
              required: true,
              label: 'Update date after which frequency of reminders changes. Format: YYYY-MM-DD HH:MM:SS.',
          },
          {
            key: 'scheduler_db_internal_tag',
            required: true,
            label: 'scheduler database internal tag of the entry that should be updated',
            choices: { 
              'vp-01-01c' : 'VP-01 flow',
              'vp-02-01c': 'VP-02-01c: catch start date webhook',
              'vp-02-01i': 'VP-02-01i send delayer',
              'vp-02-01g': 'VP-02-01g QCL and 2d invoice',
              'vp-02-01h': 'VP-02-01h 2d invoice to todoist and slack',
              'pm-03-01' : 'weekly reminders',
              'ycb-reminders' : 'Youcanbookme: send reminders before appointment',
              'pm-05-03' : 'Ask PM and QCL if toilet needs removal',
              'pm-05-02' : 'Ask PM and QCL if toilet needs to be ordered'
            }
          },
      ],
    }
  }

  