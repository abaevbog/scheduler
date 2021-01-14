import express from 'express';
import morgan from 'morgan';
import {DateTime} from 'luxon';
import  {addToReminder, updateReminderEntries, removeReminderEntries} from '../api/reminder';
import  {addToDelayer, updateDelayerEntries, removeDelayerEntries} from '../api/delayer';
import {runReminderWorkflow} from '../scheduling/reminder';
import {runDelayerWorkflow} from '../scheduling/delayer';

const schedule = require('node-schedule');

const app = express();
app.use(express.json());
morgan.token('body', (req:any, res:any) => JSON.stringify(req.body));
morgan.token('timestamp', (req:any, res:any) => {
  return DateTime.local().toString();
});
const port = 80;

app.listen(port, () => {
  console.log(`App listening at port ${port}`)
})
app.use('/', (morgan(':method :timestamp :url :status :response-time ms :body') as any) )

app.post('/delayer',(req:any, res:any) => {
  addToDelayer(req, res);
})

app.patch('/delayer',(req:any, res:any) => {
  updateDelayerEntries(req, res);
}) 

app.delete('/delayer',(req:any, res:any) => {
  removeDelayerEntries(req, res);
}) 

app.post('/reminder',(req:any, res:any) => {
  addToReminder(req, res);
})

app.patch('/reminder',(req:any, res:any) => {
  updateReminderEntries(req, res);
}) 

app.delete('/reminder',(req:any, res:any) => {
  removeReminderEntries(req, res);
}) 


app.get('/check', (req:any, res:any) => {
  res.send('I am running!')
})



schedule.scheduleJob('0 17 ? * 0,4-6', function(){
  runDelayerWorkflow()
});

schedule.scheduleJob('0 17 ? * 0,4-6', function(){
  runReminderWorkflow()
});