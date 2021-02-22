import { db } from "../service/database";
import { Request, Response } from "express";
import { dealWithPromise } from "../helpers/dealWithPromise";
import { FilterQuery } from "mongodb";
// This is the interface for the message data
interface Delayer {
  _id : string,
  projectId: string;
  tag: string;
  url: string | undefined;
  onHold: boolean | undefined;
  dueDate: Date | undefined;
  keyDate: Date | undefined;
  daysBeforeKeyDate: number | undefined;
  [prop: string]: any;
}

const addToDelayer = function (req: Request, res: Response): void {
  if (req.body.dueDate) req.body.dueDate = new Date(req.body.dueDate);
  if (req.body.keyDate) req.body.keyDate = new Date(req.body.keyDate);
  let body: Delayer = req.body;
  body.onHold = false;
  body.createdAt = new Date();
  body._id = req.body.projectId + "_" +req.body.tag;
  dealWithPromise(db.collection("Delayer").insertOne(body), res);
};

const updateDelayerEntries = function (req: Request, res: Response): void {
  let body: Delayer = req.body;
  if (body.keyDate) body.keyDate = new Date(body.keyDate);
  
  let filterStatement : FilterQuery<any> = { $and: [ { projectId: body.projectId }] };
  if (body.tag) {
    filterStatement = { $and: [ { projectId: body.projectId}, {tag: body.tag}] }
  }
  dealWithPromise(
    db
      .collection("Delayer")
      .updateMany(
        filterStatement,
        {$set: body}
      ),
    res
  );
};

const removeDelayerEntries = function (req: Request, res: Response): void {
  let body: Delayer = req.body;
  let filterStatement : FilterQuery<any> = { $and: [ { projectId: body.projectId }] };
  if (body.tag) {
    filterStatement = { $and: [ { projectId: body.projectId}, {tag: body.tag}] }
  }
  dealWithPromise(
    db.collection("Delayer").deleteMany(filterStatement),
    res
  );
};



export { addToDelayer, updateDelayerEntries, removeDelayerEntries, Delayer };
