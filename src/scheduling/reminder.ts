import { db } from "../service/database";
const axios = require("axios").default;

const runReminderWorkflow = function (): void {
  const fixedNow = new Date();

  const ensureAllDueDatesAreCorrect = function (): Promise<any> {
    return db
      .collection("Reminder")
      .updateMany(
        { $and: [{ keyDate: { $exists: true } }, { started: false }] },
        [
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
        ]
      );
  };

  const deleteSatisfiedAndOldActions = function (): Promise<any> {
    return db.collection("Reminder").deleteMany({
      $and: [{ lastDate: { $lte: "$$NOW" } }, { requiredFields: { $size: 0 } }],
    });
  };

  const executeDueActions = async function (): Promise<any[]> {
    //fetch due actions
    const dueActions = await db
      .collection("Reminder")
      .find({ dueDate: { $lte: fixedNow } })
      .toArray();
    // send them to specified url
    const promises = [];
    for (const record of dueActions) {
      console.log(record);
      promises.push(axios.post(record.url, record));
    }
    return Promise.all(promises);
  };

  const rescheduleActions = function (): Promise<any> {
    console.log("start");
    return db
      .collection("Reminder")
      .updateMany({ dueDate: { $lte: fixedNow } }, [
        {
          $set: {
            dueDate: {
              $add: [
                "$$NOW",
                {
                  $multiply: [
                    {
                      $function: {
                        body: `function ( recurrence, keyDate){
                    let index = -1;
                    let tempDate = keyDate;
                    const now = fixedNow();
                    do {
                      index++;
                      tempDate = keyDate
                    } while (
                      index < recurrence.length - 1 &&
                      now > function(){ tempDate.setDate(tempDate.getDate() - recurrence[index].daysBeforeKeyDate );return tempDate }()
                    );
                    return recurrence[index].frequency;
                  }`,
                        args: ["$recurrence", "$keyDate", "$$NOW"],
                        lang: "js",
                      },
                    },
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
      ]);
  };



  ensureAllDueDatesAreCorrect();
  deleteSatisfiedAndOldActions();
  executeDueActions();
  rescheduleActions();
};


export {runReminderWorkflow }