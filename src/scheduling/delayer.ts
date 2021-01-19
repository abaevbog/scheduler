import { db } from "../service/database";
const axios = require("axios").default;

const runDelayerWorkflow = async function (): Promise<void> {
  const fixedNow = new Date();

  const ensureAllDueDatesAreCorrect = function (): Promise<any> {
    return db.collection("Delayer").updateMany({ keyDate: { $ne: null } }, [
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
      .find({$and : [{ dueDate: { $lte: fixedNow }}, {onHold : false} ]})
      .toArray();
    // send them to specified url
    console.log("Delayer: due -- ", dueActions);
    const promises = [];
    for (const record of dueActions) {
      promises.push(axios.post(record.url, record));
    }
    return Promise.all(promises);
  };

  const deleteOldActions = function (): Promise<any> {
    return db
      .collection("Delayer")
      .deleteMany({$and : [{ dueDate: { $lte: fixedNow }}, {onHold : false} ]} );
  };

  await ensureAllDueDatesAreCorrect();
  await executeDueActions();
  await deleteOldActions();
};

export{runDelayerWorkflow };
