

const remove = (z, bundle) => {
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
    key: 'removeDelayer',
    noun: 'Rmove from Delayer ',
    display: {
      label: 'Remove from delayer',
      description: 'Delete existing entry in delayer database',
    },
    operation: {
      perform: remove,
      inputFields: [
        {
          key: 'lead_id',
          required: true,
          label: 'Lead id of the entry that will be removed',
        },
        {
            key: 'delayer_db_internal_tag',
            required: true,
            label: 'delayer database internal tag of the entry that will be removed',
            choices: { 
              'vp-01-01c' : 'VP-01 flow',
              'vp-02-01c': 'VP-02-01c: catch start date webhook',
              'vp-02-01i': 'VP-02-01i send delayer',
              'vp-02-01g': 'VP-02-01g QCL and 2d invoice',
              'vp-02-01h': 'VP-02-01h 2d invoice to todoist and slack',
              'pm-03-01' : 'weekly reminders',
              'ycb-reminders' : 'Youcanbookme: send reminders before appointment'
            }
        }
      ],
    }
  }

  