import { db } from "../service/database";
import { Request, Response } from "express";
import { dealWithPromise } from "../helpers/dealWithPromise";

interface Recurrence {
  daysBeforeKeyDate: number;
  frequency: number;
}

// This is the interface for the message data
interface Reminder {
  _id: string;
  projectId: string;
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
  if (req.body.dueDate) req.body.dueDate = new Date(req.body.dueDate);
  if (req.body.keyDate) req.body.keyDate = new Date(req.body.keyDate);
  if (req.body.lastDate) req.body.lastDate = new Date(req.body.lastDate);
  let body: Reminder = req.body;
  body.ohHold = false;
  body.started = false;
  body.createdAt = new Date();
  body._id = req.body.projectId + "_" +req.body.tag;
  return dealWithPromise(db.collection("Reminder").insertOne(body), res);
};

const updateReminderEntries = function (req: Request, res: Response): void {
  req.body.dueDate = new Date(req.body.dueDate);
  if (req.body.keyDate) req.body.keyDate = new Date(req.body.keyDate);
  if (req.body.lastDate) req.body.lastDate = new Date(req.body.lastDate);
  let body: Reminder = req.body;
  if (body.requiredFields) {
    return dealWithPromise(
      db
        .collection("Reminder")
        .updateMany(
          { $and: [{ projectId: body.projectId }] },
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
        { $and: [ { projectId: body.projectId }] },
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
        $and: [{ projectId: body.projectId }],
      }),
    res
  );
};

export { addToReminder, updateReminderEntries, removeReminderEntries, Reminder, Recurrence };
