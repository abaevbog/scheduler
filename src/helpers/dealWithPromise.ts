import {Request, Response} from 'express';

const dealWithPromise  = function (promise: Promise<any>, response: Response) {
    promise.then(async (result) => {
      if (!result){
        return response.status(405).send({ "error": "Entry not found"});
      }
      response.send({"result" : result});
    })
    .catch((error) => {
      console.log(error);
      response.status(403).send({"error" : error});
    })
  }

export{dealWithPromise}