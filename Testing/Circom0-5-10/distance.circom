template distanceAB(dimension){
    signal private input pointA[dimension];
    signal private input pointB[dimension];
    signal output dist;

    // distance : sqrt(a^2 + b^2)
    // a: xA - xB
    // b: yA - yB

    // assign the coordinates to simple variables to perform sqrt()
    var xA = pointA[0];
    var yA = pointA[1];
    var xB = pointB[0];
    var yB = pointB[1];

    // distance
    var apow2 = (xA - xB) * (xA - xB);
    var bpow2 = (yA - xB) * ( yA - yB);
    var d = sqrt(apow2 + bpow2);

    // out
    out <-- 2;
}

component main = distanceAB(2);