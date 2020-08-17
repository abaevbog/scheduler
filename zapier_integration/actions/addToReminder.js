

const addToReminder= (z, bundle) => {
    const uniqueSet = new Set(bundle.inputData.required_salesforce_fields);
    bundle.inputData.required_salesforce_fields = [...uniqueSet];

    var body = bundle.inputData;
    body.trigger_date_definition = [body.days_before_start,body.next_date];
    body.cutoff = [body.cutoff,body.frequency_in_days_before_cutoff,body.frequency_in_days_after_cutoff];
    delete body.days_before_start;
    delete body.next_date;
    delete body.frequency_in_days_before_cutoff;
    delete body.frequency_in_days_after_cutoff;

    const promise = z.request({
        url:'https://9b8pw4g950.execute-api.us-east-1.amazonaws.com/v2/add',
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
    key: 'addToReminder',
    noun: 'addToReminder',
    display: {
      label: 'Add new Reminder',
      description: 'Add entry to reminders database.',
    },
    operation: {
      perform: addToReminder,
      inputFields: [
        {
          key: 'lead_id',
          required: true,
          label: 'ID of the lead',
        },
        {
          key: 'tag',
          required: true,
          label: 'Tag that defines what zap the event triggers',
          dynamic: 'find_codes.id.name'
        },
        {
          key: 'project_name',
          required: true,
          label: 'Name of the project (without date).',
        },
        {
          key: 'next_date',
          required: false,
          label: 'Date of the next action. Format: YYYY-MM-DD HH:MM:SS.',
          helpText: 'If specified with Days Before Start, this value may be overwritten based if start date changes.'
        },
        {
          key: 'days_before_start',
          required: false,
          label: 'Number of days before predemo(if exists) when the first reminder should go.',
          helpText: `If this value is specified, date when event is triggered will be recalculated like that: trigger_date = precon/predemo - days_before start.
          If the start date is postponed, the reminders will stop until start_date - <value of this field> to send reminders again.`,
        },
        {
          key: 'indefinite',
          required: true,
          label: 'If the value is set to True, the record cannot expire and will keep going until satisfied.',
          choices:{true:true, false:false }
        },
        {
            key: 'cutoff',
            required: true,
            label: 'Number of days before predemo(if present)/precon when the reminders frequency changes.',
            helpText: "The actual date will depend on the start date and will be adjusted accordingly if start date changes so that cutoff = start_date - <Value of this field>"
        },
        {
            key: 'frequency_in_days_before_cutoff',
            required: true,
            label: 'Frequency with which action is repeated before cutoff date. Integer.',
            helpText: 'E.g. if you choose 5, action is triggered every 5 days.'
        },
        {
            key: 'frequency_in_days_after_cutoff',
            required: true,
            label: 'Frequency with which action is repeated after cutoff date. Integer.',
            helpText: 'E.g. if you choose 5, action is triggered every 5 days.'
        },
        {
            key: 'required_salesforce_fields',
            required: true,
            list: true,
            label: 'Fields from Saleforce required for the entry to be satisfied. If no comparison with salesforce is required, chooce None.',
            choices: {basic_selections_submitted__c: 'basic_selections_submitted__c',
                        conf_start_date_form_subm__c: 'conf_start_date_form_subm__c', 
                        cup_audience__c: 'cup_audience__c', feedback_submitted__c: 'feedback_submitted__c', 
                        goq_audiences__c: 'goq_audiences__c', info_request_1_submitted__c: 'info_request_1_submitted__c', 
                        info_request_2_submitted__c: 'info_request_2_submitted__c', isconverted: 'isconverted', 
                        isdeleted: 'isdeleted', isunreadbyowner: 'isunreadbyowner', 
                        major_demolition__c: 'major_demolition__c', on_hold__c: 'on_hold__c', 
                        past_app_audience__c: 'past_app_audience__c', 
                        project_completed__c: 'project_completed__c', 
                        project_prep_form_submitted__c: 'project_prep_form_submitted__c', 
                        sale_submitted__c: 'sale_submitted__c', start_date_confirmed__c: 'start_date_confirmed__c',
                        none:'none'}
        },
        {
          key: 'additional_info',
          required: false,
          label: 'Any additional information',
        },
      ],
    }
  }

  