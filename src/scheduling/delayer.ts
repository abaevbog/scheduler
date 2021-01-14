import { db } from "../service/database";
const axios = require("axios").default;

const runDelayerWorkflow = function (): void {
  const fixedNow = new Date();

  const ensureAllDueDatesAreCorrect = function (): Promise<any> {
    return db.collection("Delayer").updateMany({ keyDate: { $exists: true } }, [
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

  const executeDueActions = async function (): Promise<any[]> {
    //fetch due actions
    const dueActions = await db
      .collection("Delayer")
      .find({ dueDate: { $lte: fixedNow } })
      .toArray();
    // send them to specified url
    const promises = [];
    for (const record of dueActions) {
      promises.push(axios.post(record.url, record));
    }
    return Promise.all(promises);
  };

  const deleteOldActions = function (): Promise<any> {
    return db
      .collection("Delayer")
      .deleteMany({ dueDate: { $lte: fixedNow } });
  };

  ensureAllDueDatesAreCorrect();
  executeDueActions();
  deleteOldActions();
};

export{runDelayerWorkflow };
