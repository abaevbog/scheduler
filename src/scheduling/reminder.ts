import { DeleteWriteOpResultObject, UpdateWriteOpResult } from "mongodb";
import { db } from "../service/database";
const axios = require("axios").default;

// Function that runs the whole scheduling workflow for reminders
const runReminderWorkflow = async function (): Promise<void> {
  const fixedNow = new Date();

  // NOT USED: but it updates the dueDate to be keyDate - daysBeforeKeyDate if present
  const ensureAllDueDatesAreCorrect = function (): Promise<UpdateWriteOpResult> {
    return db
      .collection("Reminder")
      .updateMany({ $and: [{ keyDate: { $ne: null } }, { started: false }] }, [
        {
          $set: {
            dueDate: {
              $subtract: [
                "$keyDate",
                { $multiply: ["$daysBeforeKeyDate", 1000, 60, 60, 24] },
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
  const executeDueActions = async function (): Promise<any[]> {
    //fetch due actions
    const dueActions = await db
      .collection("Reminder")
      .find({ $and: [{ dueDate: { $lte: fixedNow } }, { onHold: false }] })
      .toArray();
    console.log("Reminder: due -- ", dueActions);
    // send them to specified url
    const promises = [];
    for (const record of dueActions) {
      console.log(record);
      promises.push(axios.post(record.url, record));
    }
    return Promise.all(promises);
  };

  // reschedules reminding actions
  const rescheduleActions = function (): Promise<any> {
    return (
      db
        .collection("Reminder")
        // Actions that were due
        .updateMany(
          { $and: [{ dueDate: { $lte: fixedNow } }, { onHold: false }] },
          [
            {
              //set due date to be NOW + last entry in recurrence array that
              // is greater than current time
              $set: {
                dueDate: {
                  $add: [
                    "$$NOW",
                    {
                      // finding that last entry here
                      $multiply: [
                        {
                          $function: {
                            body: `function ( recurrence, keyDate){
                    let index = -1;
                    let tempDate = keyDate;
                    const now = new Date();
                    do {
                      index++;
                      tempDate = keyDate
                    } while (
                      index < recurrence.length - 1 &&
                      now > function(){ tempDate.setDate(tempDate.getDate() - recurrence[index].daysBeforeKeyDate );return tempDate }()
                    );
                    return recurrence[index].frequency;
                  }`,
                            args: ["$recurrence", "$keyDate"],
                            lang: "js",
                          },
                        },
                        // multiply our value (e.g 10) by these numbers to get days in miliseconds
                        1000,
                        60,
                        60,
                        24,
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
