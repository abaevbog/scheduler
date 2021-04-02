let reschedule = function (recurrence, keyDate){
    let index = -1;
    let tempDate = keyDate;
    const now = new Date();
    do {
      index++;
      tempDate = keyDate
    } while (
      index < recurrence.length - 1 &&
      now > keyDate.getTime() - recurrence[index].daysBeforeKeyDate * (24*60*60*1000)
    );
    return recurrence[index].frequency;
  }


let recurrence = [{'frequency':7,'daysBeforeKeyDate':28},{'frequency':4,'daysBeforeKeyDate':14},{'frequency':2,'daysBeforeKeyDate':5}]
let keyDate = new Date('2021-04-13T12:30:00.000+00:00')

console.log(reschedule(recurrence, keyDate))
