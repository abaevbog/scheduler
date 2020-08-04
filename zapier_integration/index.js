var oneTime = require('./actions/oneTimeAction');
var delayerUpdate = require('./actions/updateDelayer');
var delayerDelete = require('./actions/deleteFromDelayer');
var recurring = require('./actions/recurringAction');
var recurringDelete = require('./actions/deleteRecurringAction');
var update = require('./actions/updateReminders');
var test = require('./actions/testUpdate');
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
    [oneTime.key] : oneTime,
    [recurring.key]: recurring,
    [update.key]: update,
    [delayerUpdate.key] : delayerUpdate,
    [delayerDelete.key] : delayerDelete,
    [recurringDelete.key]: recurringDelete
  },

  resources: {},
};
