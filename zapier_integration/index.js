var addToDelayer = require('./actions/addToDelayer');
var addToReminder = require('./actions/addToReminder');
var deleteFromReminder = require('./actions/deleteFromReminder');
var deleteFromDelayer = require('./actions/deleteFromDelayer');
var fetchCodes = require('./triggers/fetch_codes');

module.exports = {
  // This is just shorthand to reference the installed dependencies you have.
  // Zapier will need to know these before we can upload.
  version: require('./package.json').version,
  platformVersion: require('zapier-platform-core').version,

  // If you want your trigger to show up, you better include it here!
  triggers: {
    [fetchCodes.key] : fetchCodes
  },

  // If you want your searches to show up, you better include it here!
  searches: {},

  // If you want your creates to show up, you better include it here!
  creates: {
    [addToDelayer.key] : addToDelayer,
    [addToReminder.key]: addToReminder,
    [deleteFromReminder.key]: deleteFromReminder,
    [deleteFromDelayer.key] : deleteFromDelayer,
  },

  resources: {},
};
