const listCodes = (z, bundle) => {
    const promise = z.request(
        'https://usx0yjoww7.execute-api.us-east-1.amazonaws.com/dev/codes'
    )
    return promise.then(response => response.json)
  }  


  module.exports = {
    key: 'find_codes',
    noun: 'Codes',
    display: {
      label: 'Get Codes',
      description: 'Choose the code',
      hidden: true
    },
    operation: {
      perform: listCodes,
      inputFields: [ ],
    }
  }