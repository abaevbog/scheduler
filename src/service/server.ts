import express from "express";
import morganBody from 'morgan-body';
import {
  addToReminder,
  updateReminderEntries,
  removeReminderEntries,
} from "../api/reminder";
import {
  addToDelayer,
  updateDelayerEntries,
  removeDelayerEntries,
} from "../api/delayer";
import { runReminderWorkflow } from "../scheduling/reminder";
import { runDelayerWorkflow } from "../scheduling/delayer";
import schedule from "node-schedule";
import { body, validationResult, oneOf } from "express-validator";

const app = express();
app.use(express.json());

const port = 80;

app.listen(port, () => {
  console.log(`App listening at port ${port}`);
});
morganBody(app);
app.post(
  "/delayer",
  body("tag").exists(),
  body("projectName").exists(),
  oneOf([body("dueDate").isISO8601(), body("keyDate").isISO8601()]),
  body("url").isURL(),
  (req: any, res: any) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }

    addToDelayer(req, res);
  }
);

app.patch(
  "/delayer",
  body("tag").exists(),
  body("projectName").exists(),
  oneOf([body("dueDate").isISO8601(), body("keyDate").isISO8601()]),
  (req: any, res: any) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }

    updateDelayerEntries(req, res);
  }
);

app.delete(
  "/delayer",
  body("tag").exists(),
  body("projectName").exists(),
  (req: any, res: any) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }

    removeDelayerEntries(req, res);
  }
);

app.post(
  "/delayer/run",
  (req: any, res: any) => {
    runDelayerWorkflow();
    res.send("Running delayer workflow")
  }
);

app.post(
  "/reminder",
  body("tag").exists(),
  body("projectName").exists(),
  oneOf([body("dueDate").isISO8601(), body("keyDate").isISO8601()]),
  body("url").isURL(),
  body("requiredFields")
    .isArray()
    .withMessage("Must Be array of required fields from Airtable"),
  body("recurrence")
    .isArray()
    .withMessage(
      "Must Be array of objects [{daysBeforeKeyDate:int,frequency:int}]"
    ),
  (req: any, res: any) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }

    addToReminder(req, res);
  }
);

app.patch(
  "/reminder",
  body("tag").exists(),
  body("projectName").exists(),
  (req: any, res: any) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }
    updateReminderEntries(req, res);
  }
);

app.delete(
  "/reminder",
  body("tag").exists(),
  body("projectName").exists(),
  (req: any, res: any) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }
    removeReminderEntries(req, res);
  }
);

app.post(
  "/reminder/run",
  (req: any, res: any) => {
    runReminderWorkflow();
    res.send("Running reminder workflow")
  }
);



app.get("/check", (req: any, res: any) => {
  res.send("I am running!");
});


let delayerRule = new schedule.RecurrenceRule();
delayerRule.tz = 'America/New_York'
delayerRule.hour =  [new schedule.Range(8, 17)];
delayerRule.minute = 0;

let reminderRule = new schedule.RecurrenceRule();
reminderRule.tz = 'America/New_York'
reminderRule.dayOfWeek = [new schedule.Range(1, 5)];
reminderRule.hour =  [new schedule.Range(8, 17)];
reminderRule.minute = 0;

schedule.scheduleJob(delayerRule, function () {
  console.log("Delayer just ran: ", new Date())
  runDelayerWorkflow();
});

schedule.scheduleJob(reminderRule, function () {
  console.log("Reminder just ran: ", new Date())
  runReminderWorkflow();
});


