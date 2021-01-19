import {db} from '../service/database';
import {delayerEntries} from './seed';
import {runDelayerWorkflow } from '../scheduling/delayer';

setTimeout(async () => {
    await db.collection('Delayer').deleteMany({});
    let promises:Promise<any>[] = [];
    delayerEntries.forEach((entry:any) => {
        promises.push(db.collection("Delayer").insertOne(entry));
    })
    Promise.all(promises).then((res:any) => {
        runDelayerWorkflow()
    })
}, 5000)
