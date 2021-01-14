import { db } from "../service/database";
import { Request, Response } from "express";
import { dealWithPromise } from "../helpers/dealWithPromise";

interface Recurrence {
  daysBeforeKeyDate: number;
  frequency: number;
}

// This is the interface for the message data
interface Reminder {
  id: number;
  projectName: string;
  tag: string;
  url: string | undefined;
  onHold: boolean;
  dueDate: Date;
  keyDate: Date | undefined;
  daysBeforeKeyDate: number | undefined;
  lastDate: Date | undefined;
  started: boolean;
  recurrence: Recurrence[];
  requiredFields: string[] | undefined;
  [prop: string]: any;
}

const addToReminder = function (req: Request, res: Response): void {
  let body: Reminder = req.body;
  return dealWithPromise(db.collection("Reminder").insertOne(body), res);
};

const updateReminderEntries = function (req: Request, res: Response): void {
  let body: Reminder = req.body;
  // if we have a required field, remove it
  if (body.requiredFields) {
    return dealWithPromise(
      db
        .collection("Reminder")
        .updateMany(
          { $and: [{ tag: body.tag }, { projectName: body.projectName }] },
          { $pull: { requiredFields: body.requiredFields } } 
        ),
      res
    );
  } 
  // otherwise, we are updating other fields so just put the new object in
  dealWithPromise(
    db
      .collection("Reminder")
      .updateMany(
        { $and: [{ tag: body.tag }, { projectName: body.projectName }] },
        {$set : body}
      ),
    res
  );
};

const removeReminderEntries = function (req: Request, res: Response): void {
  let body: Reminder = req.body;
  dealWithPromise(
    db
      .collection("Reminder")
      .deleteMany({
        $and: [{ tag: body.tag }, { projectName: body.projectName }],
      }),
    res
  );
};

export { addToReminder, updateReminderEntries, removeReminderEntries, Recurrence };
