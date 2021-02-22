import { db } from "../service/database";
import { Request, Response } from "express";
import { dealWithPromise } from "../helpers/dealWithPromise";
import { FilterQuery, UpdateQuery } from "mongodb";

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
  body.onHold = false;
  body.started = false;
  body.createdAt = new Date();
  body._id = req.body.projectId + "_" +req.body.tag;
  return dealWithPromise(db.collection("Reminder").insertOne(body), res);
};



const updateReminderEntries = function (req: Request, res: Response): void {
  if (req.body.dueDate) req.body.dueDate = new Date(req.body.dueDate);
  if (req.body.keyDate) req.body.keyDate = new Date(req.body.keyDate);
  if (req.body.lastDate) req.body.lastDate = new Date(req.body.lastDate);
  let body: Reminder = req.body;

  // Update everything for entries with this project id and tag
  if (body.tag) {
    return dealWithPromise(
      db
        .collection("Reminder")
        .updateMany(
          { $and: [ { projectId: body.projectId}, {tag: body.tag}] },
          {$set : body}
        ),
      res
    );
  }
    // Update key start date for entries that have this projectId IF START DATE EXISTS
  if (body.keyDate) {
    dealWithPromise(
      db
        .collection("Reminder")
        .updateMany(
        { $and: [ { projectId: body.projectId}, { keyDate: { $ne: null } }] },
        {$set : {keyDate : body.keyDate, started: false, onHold: body.onHold || false}}
        ),
      res
    );
  }

  // Update last date for entries that have this projectId IF LAST DATE EXISTS
  if (body.lastDate) {
    dealWithPromise(
      db
        .collection("Reminder")
        .updateMany(
        { $and: [ { projectId: body.projectId}, { lastDate: { $ne: null } }] },
        {$set : {lastDate : body.lastDate, started: false, onHold: body.onHold || false}}
        ),
      res
    );
  }
};

const removeReminderEntries = function (req: Request, res: Response): void {
  let body: Reminder = req.body;
  let filterStatement : FilterQuery<any> = { $and: [ { projectId: body.projectId }] };
  if (body.tag) {
    filterStatement = { $and: [ { projectId: body.projectId}, {tag: body.tag}] }
  }
  dealWithPromise(
    db
      .collection("Reminder")
      .deleteMany(filterStatement),
    res
  );
};

const fetchReminderEntry = function (req: Request, res: Response): void {
  let parameters : {projectId : string, tag: string} = req.query as {projectId : string, tag: string};
  dealWithPromise(
    db
      .collection("Reminder").findOne({$and: [{ projectId: parameters.projectId }, {tag: parameters.tag} ]}),
    res
  );
};


export { addToReminder, updateReminderEntries, fetchReminderEntry, removeReminderEntries, Reminder, Recurrence };
