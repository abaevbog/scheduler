import  {addToReminder, Reminder} from '../api/reminder';
import  {addToDelayer, Delayer } from '../api/delayer';

const delayerEntries: Delayer[] = [
    {
        _id : '1',
        projectName : 'project',
        tag : 'pm-01',
        url : 'https://hook.integromat.com/2ajmoqs3s78bq1ohpz64nt0029jssf0u',
        onHold : false,
        dueDate : new Date('2021-01-17T20:42:12.663Z'),
        keyDate : undefined,
        daysBeforeKeyDate: undefined,
        comment : 'nothing should happen'
    },
    {
        _id : '2',
        projectName : 'project',
        tag : 'pm-01',
        url : 'https://hook.integromat.com/2ajmoqs3s78bq1ohpz64nt0029jssf0u',
        onHold : false,
        dueDate : new Date('2021-01-12T20:42:12.663Z'),
        keyDate : undefined,
        daysBeforeKeyDate: undefined,
        comment : 'due'
    },
    {
        _id : '3',
        projectName : 'project',
        tag : 'pm-01',
        url : 'https://hook.integromat.com/2ajmoqs3s78bq1ohpz64nt0029jssf0u',
        onHold : false,
        dueDate : new Date('2021-01-12T20:42:12.663Z'),
        keyDate : new Date('2021-01-20T20:42:12.663Z'),
        daysBeforeKeyDate: 10,
        comment : 'reschedule is due. Date should be 10'
    }
]

const reminderEntries: Reminder[] = [
    {
        _id : '1',
        projectName : 'project',
        tag : 'pm-01',
        url : 'https://hook.integromat.com/2ajmoqs3s78bq1ohpz64nt0029jssf0u',
        onHold : false,
        dueDate : new Date('2021-01-18T20:42:12.663Z'),
        keyDate : new Date('2021-01-28T20:42:12.663Z'),
        daysBeforeKeyDate: 10,
        started : false, 
        lastDate : new Date('2021-01-28T20:42:12.663Z'),
        requiredFields : ['one', 'two', 'three'],
        recurrence : [{daysBeforeKeyDate : 5, frequency : 5}],
        comment : 'Do no do anything',
    },
    {
        _id : '2',
        projectName : 'project',
        tag : 'pm-01',
        url : 'https://hook.integromat.com/2ajmoqs3s78bq1ohpz64nt0029jssf0u',
        onHold : false,
        dueDate : new Date('2021-01-03T20:42:12.663Z'),
        keyDate : new Date('2021-01-28T20:42:12.663Z'),
        daysBeforeKeyDate: 10,
        started : false, 
        lastDate : new Date('2021-01-28T20:42:12.663Z'),
        requiredFields : [],
        recurrence : [{daysBeforeKeyDate : 5, frequency : 5}],
        comment : 'Satisfied/No required fields',
    },
    {
        _id : '3',
        projectName : 'project',
        tag : 'pm-01',
        url : 'https://hook.integromat.com/2ajmoqs3s78bq1ohpz64nt0029jssf0u',
        onHold : false,
        dueDate : new Date('2021-01-03T20:42:12.663Z'),
        keyDate : new Date('2021-01-28T20:42:12.663Z'),
        daysBeforeKeyDate: 10,
        started : false, 
        lastDate : new Date('2019-01-28T20:42:12.663Z'),
        requiredFields : ['one', 'two', 'three'],
        recurrence : [{daysBeforeKeyDate : 5, frequency : 5}],
        comment : 'Satisfied/past last date',
    },
    {
        _id : '4',
        projectName : 'project',
        tag : 'pm-01',
        url : 'https://hook.integromat.com/2ajmoqs3s78bq1ohpz64nt0029jssf0u',
        onHold : false,
        dueDate : new Date('2021-01-03T20:42:12.663Z'),
        keyDate : new Date('2021-01-28T20:42:12.663Z'),
        daysBeforeKeyDate: 25,
        started : false, 
        lastDate : new Date('2021-01-28T20:42:12.663Z'),
        requiredFields : ['one', 'two', 'three'],
        recurrence : [{daysBeforeKeyDate : 5, frequency : 5}],
        comment : 'Due, executed and rescheduled 5 days from now',
    },
    {
        _id : '5',
        projectName : 'project',
        tag : 'pm-01',
        url : 'https://hook.integromat.com/2ajmoqs3s78bq1ohpz64nt0029jssf0u',
        onHold : false,
        dueDate : new Date('2021-01-03T20:42:12.663Z'),
        keyDate : new Date('2021-01-28T20:42:12.663Z'),
        daysBeforeKeyDate: 25,
        started : false, 
        lastDate : new Date('2021-01-28T20:42:12.663Z'),
        requiredFields : ['one', 'two', 'three'],
        recurrence : [{daysBeforeKeyDate : 20, frequency : 7},{daysBeforeKeyDate : 10, frequency : 3}],
        comment : 'Due rescheduled for 3 days later',
    }
]

export {delayerEntries, reminderEntries}