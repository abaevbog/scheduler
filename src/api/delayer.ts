import {db} from '../service/database';
import {Request, Response} from 'express';
import {dealWithPromise} from '../helpers/dealWithPromise'
// This is the interface for the message data
interface Delayer {
  projectName: string;
  tag : string;
  url : string | undefined;
  onHold : boolean | undefined;
  dueDate : Date | undefined;
  keyDate : Date | undefined;
  daysBeforeKeyDate : number | undefined;
  [prop: string]: any;
}

const addToDelayer = function (req:Request, res : Response) : void {
    let body: Delayer = req.body;
    dealWithPromise(db.collection('delayer').insertOne(body), res);
}

const updateDelayerEntries = function (req:Request, res : Response) : void {
    let body:Delayer = req.body;
    dealWithPromise(db.collection('delayer').updateMany( {$and : [{tag : body.tag}, {projectName: body.projectName} ] },body),res);
}

const removeDelayerEntries = function (req:Request, res : Response) : void {
    let body:Delayer = req.body;
    dealWithPromise(db.collection('delayer').deleteMany( {$and : [{tag : body.tag}, {projectName: body.projectName} ] }),res);
}

export {addToDelayer, updateDelayerEntries, removeDelayerEntries}