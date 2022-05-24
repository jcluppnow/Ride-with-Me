// Calculate the as-the-crow-flies distance between two points
// Derived from https://en.wikipedia.org/wiki/Haversine_formula#Formulation
const haversineDistance = (lat1, long1, lat2, long2) => {
  const RADIUS = 6378137 // Mean radius of the earth (in metres)

  function hav (theta) {
    return Math.sin(theta / 2) ** 2
  }

  function radians (theta) {
    return (theta * Math.PI) / 180.0
  }

  const lat1Rad = radians(lat1)
  const lat2Rad = radians(lat2)
  const long1Rad = radians(long1)
  const long2Rad = radians(long2)

  const h = hav(lat2Rad - lat1Rad) + Math.cos(lat1Rad) * Math.cos(lat2Rad) * hav(long2Rad - long1Rad)
  return 2 * RADIUS * Math.asin(Math.sqrt(h))
}

const urlB64ToUint8Array = (base64String) => {
  const padding = '='.repeat((4 - base64String.length % 4) % 4)
  const base64 = (base64String + padding)
    .replace(/-/g, '+')
    .replace(/_/g, '/')

  const rawData = window.atob(base64)
  const outputArray = new Uint8Array(rawData.length)
  const outputData = outputArray.map((output, index) => rawData.charCodeAt(index))

  return outputData
}

export default {
  haversineDistance,
  urlB64ToUint8Array
}
