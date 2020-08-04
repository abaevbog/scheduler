

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
            dynamic: 'find_codes.id.name'
          },
      ],
    }
  }

  