

const addRecordToDB = (z, bundle) => {
    const uniqueSet = new Set(bundle.inputData.required_salesforce_fields);
    bundle.inputData.required_salesforce_fields = [...uniqueSet];
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
    key: 'recurringAction',
    noun: 'recurring Action',
    display: {
      label: 'Recurring Action',
      description: 'Action that should happen repeatedly in the future, like reminders.',
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
            client_form_01 : 'Client Form 01',
            client_form_02: 'Client Form 02'
          },
        },
        {
          key: 'next_action',
          required: true,
          label: 'Date of the next action. Format: YYYY-MM-DD HH:MM:SS.',
        },
        {
            key: 'event_date',
            required: true,
            label: 'Date of the key event after which the action is no longer repeated regardless of salesforce fields. Format: YYYY-MM-DD HH:MM:SS.',
        },
        {
            key: 'cutoff',
            required: true,
            label: 'Date after which frequency of reminders changes. Format: YYYY-MM-DD HH:MM:SS.',
        },
        {
            key: 'frequency_in_days_before_cutoff',
            required: true,
            label: 'Frequency with which action is repeated before cutoff date. Integer. E.g. if you choose 5, action is triggered every 5 days.',
        },
        {
            key: 'frequency_in_days_after_cutoff',
            required: true,
            label: 'Frequency with which action is repeated after cutoff date. Integer. E.g. if you choose 5, action is triggered every 5 days.',
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

  