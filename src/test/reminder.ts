import {reminderEntries} from './seed';
import {runReminderWorkflow } from '../scheduling/reminder';
import {db} from '../service/database';

setTimeout(async () => {
    await db.collection('Reminder').deleteMany({});
    let promises:Promise<any>[] = [];
    reminderEntries.forEach((entry:any) => {
        promises.push(db.collection("Reminder").insertOne(entry));
    })
    Promise.all(promises).then((res:any) => {
        runReminderWorkflow()
    })
}, 5000)
