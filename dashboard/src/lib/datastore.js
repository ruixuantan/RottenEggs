const documentaryStore = [];
const indiefilmStore = [];
const consumeallStore = [];


export function addEvent(service) {
  const timeNow = Date.now();
  switch(service) {
    case "documentary":
      documentaryStore.push(timeNow);
      return;
    case "indiefilm":
      indiefilmStore.push(timeNow);
      return;
    case "consumeall":
      consumeallStore.push(timeNow);
      return;
    default:
      console.error(`${service} not recognised`)
      return;
  }
}

function calculateRate(store) {
  if (store.length == 0) {
    return 0;
  }
  const interval = (store[store.length - 1] - store[0]) / 1000;
  const rate = (store.length - 1) / interval;
  store.length = 0;
  return rate;
}

export function calculateRates() {
  return {
    documentary: calculateRate(documentaryStore),
    indiefilm: calculateRate(indiefilmStore),
    consumeall: calculateRate(consumeallStore),
  }
}
