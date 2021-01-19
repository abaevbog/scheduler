import { MongoClient, Db } from "mongodb";

const uri = process.env.MONGO_URL || "mongodb://localhost:27017/scheduler";
let db : Db;

const establishConnection = function():void {
    var client = new MongoClient(uri, { useUnifiedTopology: true });
    client.connect().then((res) => {
        console.log("connected");
        db = client.db('scheduler');
    }).catch((e) => {
        console.log(e);
        console.log("Retry in 90 seconds");
        setTimeout(establishConnection,90000)
    })
} 
establishConnection();


export {db}
