

const addToDelayer = (z, bundle) => {
    var body = bundle.inputData;
    body.trigger_date_definition = [body.days_before_start,body.next_date];
    delete body.days_before_start;
    delete body.next_date;

    const promise = z.request({
        url:'https://9b8pw4g950.execute-api.us-east-1.amazonaws.com/v2/add',
        method: 'POST',
        body: body,
        params: {
          "operator": "delayer"
        },
        headers: {
          'Authorization' : 'bmasters2020'
          }
        }
    )
    return promise.then(response => response.json)
  }  


  module.exports = {
    key: 'addToDelayer',
    noun: 'Add entry to Delayer',
    display: {
      label: 'Single event to be tiggered in the future',
      description: 'Add entry to DB that will be triggered once in the future',
    },
    operation: {
      perform: addToDelayer,
      inputFields: [
        {
          key: 'lead_id',
          required: true,
          label: 'ID of the lead',

        },
        {
          key: 'tag',
          required: true,
          label: 'Which zap will be triggered by the event',
          dynamic: 'find_codes.id.name'
        },
        {
          key: 'project_name',
          required: true,
          label: 'Project name (without date)',
        },
        {
          key: 'next_date',
          required: false,
          label: 'Date-time when the event is triggered',
          helpText: 'If specified with Days Before Start, this value may be overwritten based if start date changes.'
        },
        {
          key: 'days_before_start',
          required: false,
          label: 'Number of days before predemo(if exists) or precon when the event should be triggered.',
          helpText: `If this value is specified, date when event is triggered will be recalculated like that: trigger_date = precon/predemo - days_before start`,
        },
        {
          key: 'additional_info',
          required: false,
          label: 'Optional additional info',
        }
      ],
    }
  }

  