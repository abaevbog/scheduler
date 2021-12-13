import { DeleteWriteOpResultObject, UpdateWriteOpResult } from "mongodb";
import { db } from "../service/database";
const axios = require("axios").default;

// Function that runs the whole scheduling workflow for reminders
const runReminderWorkflow = async function (): Promise<void> {
  const fixedNow = new Date();
  const fifteenMinutesAgo = fixedNow;
  fifteenMinutesAgo.setMinutes(fixedNow.getMinutes() - 10);
  const ensureAllDueDatesAreCorrect = function (): Promise<UpdateWriteOpResult> {
    return db
      .collection("Reminder")
      .updateMany( 
        { $and: [
          { keyDate: { $ne: null } },
          { started: false }, 
          {createdAt : {$lte: new Date((new Date().getTime() - (5 * 24 * 60 * 60 * 1000)))}}
        ]}, 
        [{
          $set: {
            dueDate: {
              $subtract: [
                "$keyDate",
                {
                  $function: {
                    body: `function (recurrence){
                      let dayBeforeStart = recurrence[0].daysBeforeKeyDate;
                      return dayBeforeStart * (24*60*60*1000);
                    }`,
                    args: ["$recurrence"],
                    lang: "js",
                  }
                },
              ],
            },
          },
        },
      ]);
  };

  // Delete actions that have empty requiredFields or that are past last date
  const deleteSatisfiedAndOldActions = async function (): Promise<DeleteWriteOpResultObject> {
    const toBeDeleted = await db
      .collection("Reminder")
      .find({
        $or: [
          { lastDate: { $lte: fixedNow } },
          { requiredFields: { $size: 0 } },
        ],
      })
      .toArray();
    console.log("Reminder: delete -- ", toBeDeleted);
    return db.collection("Reminder").deleteMany({
      $or: [{ lastDate: { $lte: fixedNow } }, { requiredFields: { $size: 0 } }],
    });
  };

  // Fetches actions that are past due and not on hold and sends requests
  const executeDueActions = async function (): Promise<any> {
    //fetch due actions
    const dueActions = await db
      .collection("Reminder")
      .find(
        { $and: [
          { dueDate: { $lte: fixedNow } }, 
          { onHold: false },
          {createdAt : {$lte: new Date((new Date().getTime() - (5 * 24 * 60 * 60 * 1000)))}}
        ] 
      })
      .toArray();
    console.log("Reminder: due -- ", dueActions);
    // send them to specified url
    const promises = [];
    for (const record of dueActions) {
      try {
        await promises.push(axios.post(record.url, record));
      } catch (e) {
        console.log("Error ", e, "Record ", record )
      }
      
    }
  };

  // reschedules reminding actions
  const rescheduleActions = function (): Promise<any> {
    return (
      db
        .collection("Reminder")
        // Actions that were due
        .updateMany(
          { $and: [ 
            { dueDate: { $lte: fixedNow } }, 
            { onHold: false },
            { createdAt : {$lte: new Date((new Date().getTime() - (5 * 24 * 60 * 60 * 1000)))}}
          ]},
          [
            {
              //set due date to be NOW + last entry in recurrence array that
              // is greater than current time
              $set: {
                dueDate: {
                  $add: [
                    fifteenMinutesAgo,
                    {
                      // finding that last entry here
                      $multiply: [
                        {
                          $function: {
                            body: `function ( recurrence, keyDate){
                              let index = -1;
                              let tempDate = keyDate;
                              const now = new Date();
                              if (!keyDate) {
                                return recurrence[0].frequency;
                              }
                              do {
                                index++;
                                if (index == recurrence.length) {
                                  break;
                                }
                                cutoff =  new Date(keyDate.getTime());
                                cutoff.setDate(cutoff.getDate() - recurrence[index].daysBeforeKeyDate)
                              } while (now > cutoff)                    
                              if (index == -1 || index == 0)
                                index = 1;
                              return recurrence[index - 1].frequency;
                            }`,
                            args: ["$recurrence", "$keyDate"],
                            lang: "js",
                          },
                        },
                        1000, // 1 second
                        60, // 1 minute
                        60, //1 hour 
                        24, //1 day
                      ],
                    },
                  ],
                },
              },
            },
            { $set: { started: true } },
          ]
        )
    );
  };

  await ensureAllDueDatesAreCorrect();
  await deleteSatisfiedAndOldActions();
  await executeDueActions();
  await rescheduleActions();
};

export { runReminderWorkflow };
