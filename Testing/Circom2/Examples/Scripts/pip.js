// MODULES
// fs: to write onto a file.json
// prime: to generate a random prime number, and a generator of the field Zp
// point: to use class Point
// raytracing: to perform functions to prove PIP
const fs = require('fs');
const prime = require('./prime');
const Point = require('./point');
const raytracing = require('./raytracing');

// TESTING EXPORTS
var p = prime.getRandPrime(1, 10);
console.log('prime: ' + p);
const p1 = new Point(0, 0);
console.log('point: ' + JSON.stringify(p1));

// SET A PRIME
// SET A GENERATOR of field Zp
// SET A POLYGON
// SET A POINT
// VERIFY PIP
// - yes: right SUM
// - no: wrong sum
// COMPUTE SUM
// COMPUTE PERIMETER

/*
CIRCOM INPUTS:
- a: sum of distances from point to sides
- b: polygon perimeter
- c: prime number
- d: generator
*/
const inputs = {
  a: 2,
  b: 4,
  c: 6,
  d: 24,
};

//fs.writeFileSync('./input.json', JSON.stringify(inputs), 'utf-8');
