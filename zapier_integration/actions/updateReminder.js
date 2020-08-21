

const updateReminder= (z, bundle) => {
    var body = bundle.inputData;
    body.trigger_date_definition = [body.days_before_start,body.next_date];
    delete body.days_before_start;
    delete body.next_date;

    const promise = z.request({
        url:'https://9b8pw4g950.execute-api.us-east-1.amazonaws.com/v2/update',
        method: 'POST',
        body: body,
        params: {
          'operator':'reminder'
        },
        headers: {
          'Authorization' : 'bmasters2020'
          }
        }
    )
    return promise.then(response => response.json)
  }  


  module.exports = {
    key: 'updateReminder',
    noun: 'updateReminder',
    display: {
      label: 'Update  Reminder',
      description: 'Update entry in reminders database',
    },
    operation: {
      perform: updateReminder,
      inputFields: [
        {
          key: 'lead_id',
          required: true,
          label: 'ID of the lead of the entry that will be updated',
        },
        {
          key: 'tag',
          required: true,
          label: 'Tag of the entry that will be udpated',
          dynamic: 'find_codes.id.name'
        },
        {
            key: 'next_date',
            required: true,
            label: 'NEW date of the next action. Format: YYYY-MM-DD HH:MM:SS.',
            helpText: 'Next action will be set to this valie'
          },
        {
          key: 'days_before_start',
          required: false,
          label: 'Number of days before predemo(if exists) when the first reminder should go.',
        },
      ],
    }
  }

  