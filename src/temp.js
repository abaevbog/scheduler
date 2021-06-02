let reschedule = function (recurrence, keyDate){
    let index = -1;
    let cutoff = new Date(keyDate.getTime());
    const now = new Date();

    do {
      index++;
      if (index == recurrence.length) {
        break;
      }
      cutoff =  new Date(keyDate.getTime());
      cutoff.setDate(cutoff.getDate() - recurrence[index].daysBeforeKeyDate)
    } while (now > cutoff)

    if (index == -1 || index == 0)
      index = 1;
    return recurrence[index - 1].frequency;
  }


let recurrence = [{'frequency':7,'daysBeforeKeyDate':28},{'frequency':4,'daysBeforeKeyDate':14},{'frequency':2,'daysBeforeKeyDate':5}]
let keyDate = new Date('2021-04-10T12:30:00.000+00:00')

console.log("result ", reschedule(recurrence, keyDate))
