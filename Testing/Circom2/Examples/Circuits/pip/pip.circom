pragma circom 2.0.4;

include "../Utils/utils.circom";

// This function returns a constant to describe an ipotethical infinity point.
function pointToInfinty(){
    return 100;
}

function maxN(x, y){
    if(x >= y) return x;
    return y;
}

function minN(x, y){
    if(x >= y) return y;
    return x;
}

template OnSegment(){
    signal input p[2];
    signal input q[2];
    signal input r[2];
    signal output out;
    
    var a = 0;
    var b = 0;

    a = p[0];
    b = r[0];
    var max1 = maxN(a, b);
    var min1 = minN(a, b);

    a = p[1];
    b = r[1];
    var max2 = maxN(a, b);
    var min2 = minN(a, b);

    component firstCheck = LessEqThan(16);
    firstCheck.in[0] <== q[0];
    firstCheck.in[1] <-- max1;

    component secondCheck = GreaterEqThan(16);
    secondCheck.in[0] <== q[0];
    secondCheck.in[1] <-- min1;

    component thirdCheck = LessEqThan(16);
    thirdCheck.in[0] <== q[1];
    thirdCheck.in[1] <-- max2;

    component fourthCheck = GreaterEqThan(16);
    fourthCheck.in[0] <== q[1];
    fourthCheck.in[1] <-- min2;

    out <-- firstCheck.out + secondCheck.out + thirdCheck.out + fourthCheck.out;
}

template Orientation(){
    signal input p[2];
    signal input q[2];
    signal input r[2];
    signal output out;

    signal partOne;
    signal partTwo;

    var result = 0;
    var exit = 0;

    partOne <== (q[1] - p[1]) * (r[0] - q[0]);
    partTwo <== (q[0] - p[0]) * (r[1] - q[1]);

    result = partOne - partTwo;
    if(result > 0) exit = 1; // clock-wise
    if(result < 0) exit = 2; // counterclock-wise
    // else is 0: collinear

    out <-- exit;
}

template Intersects(){
    signal input p1[2];
    signal input q1[2];
    signal input p2[2];
    signal input q2[2];
    signal output out;

    component o1 = Orientation();
    o1.p[0] <== p1[0];
    o1.p[1] <== p1[1];
    o1.q[0] <== q1[0];
    o1.q[1] <== q1[1];
    o1.r[0] <== p2[0];
    o1.r[1] <== p2[1];

    component o2 = Orientation();
    o2.p[0] <== p1[0];
    o2.p[1] <== p1[1];
    o2.q[0] <== q1[0];
    o2.q[1] <== q1[1];
    o2.r[0] <== q2[0];
    o2.r[1] <== q2[1];

    component o3 = Orientation();
    o3.p[0] <== p2[0];
    o3.p[1] <== p2[1];
    o3.q[0] <== q2[0];
    o3.q[1] <== q2[1];
    o3.r[0] <== p1[0];
    o3.r[1] <== p1[1];

    component o4 = Orientation();
    o4.p[0] <== p2[0];
    o4.p[1] <== p2[1];
    o4.q[0] <== q2[0];
    o4.q[1] <== q2[1];
    o4.r[0] <== q1[0];
    o4.r[1] <== q1[1];

    var check = 0;
    var result = 0;

    // General Case (o1 != o2)&(o3 != o4)
    component eq1 = IsEqual(); 
    eq1.in[0] <== o1.out;
    eq1.in[1] <== o2.out;

    component eq2 = IsEqual(); 
    eq2.in[0] <== o3.out;
    eq2.in[1] <== o4.out;

    check = eq1.out + eq2.out; 
    if(check == 0) result = 1;

    // Special Case 1: (o1 == 0)&(onSegment)
    component eq3 = IsEqual();
    eq3.in[0] <== o1.out;
    eq3.in[1] <== 0;

    component segmentCheck1 = OnSegment();
    segmentCheck1.p[0] <== p1[0];
    segmentCheck1.p[1] <== p1[1];
    segmentCheck1.q[0] <== p2[0];
    segmentCheck1.q[1] <== p2[1];
    segmentCheck1.r[0] <== q1[0];
    segmentCheck1.r[1] <== q1[1];

    check = eq3.out + segmentCheck1.out;
    if(check == 5) result = 1;

    // Special Case 2: (o2 == 0)&(onSegment)
    component eq4 = IsEqual();
    eq4.in[0] <== o2.out;
    eq4.in[1] <== 0;

    component segmentCheck2 = OnSegment();
    segmentCheck2.p[0] <== p1[0];
    segmentCheck2.p[1] <== p1[1];
    segmentCheck2.q[0] <== q2[0];
    segmentCheck2.q[1] <== q2[1];
    segmentCheck2.r[0] <== q1[0];
    segmentCheck2.r[1] <== q1[1];

    check = eq4.out + segmentCheck2.out;
    if(check == 5) result = 1;

    // Special Case 3: (o3 == 0)&(onSegment)
    component eq5 = IsEqual();
    eq5.in[0] <== o3.out;
    eq5.in[1] <== 0;

    component segmentCheck3 = OnSegment();
    segmentCheck3.p[0] <== p2[0];
    segmentCheck3.p[1] <== p2[1];
    segmentCheck3.q[0] <== p1[0];
    segmentCheck3.q[1] <== p1[1];
    segmentCheck3.r[0] <== q2[0];
    segmentCheck3.r[1] <== q2[1];

    check = eq5.out + segmentCheck3.out;
    if(check == 5) result = 1;

    // Special Case 4: (o4 == 0)&(onSegment)
    component eq6 = IsEqual();
    eq6.in[0] <== o4.out;
    eq6.in[1] <== 0;

    component segmentCheck4 = OnSegment();
    segmentCheck4.p[0] <== p2[0];
    segmentCheck4.p[1] <== p2[1];
    segmentCheck4.q[0] <== q1[0];
    segmentCheck4.q[1] <== q1[1];
    segmentCheck4.r[0] <== q2[0];
    segmentCheck4.r[1] <== q2[1];

    check = eq6.out + segmentCheck4.out;
    if(check == 5) result = 1;

    log(result);
    out <-- result;
}

template PointInPolygon(n){
    signal input point[2];
    signal input polygon[n][2];
    signal output inside;

    var extreme = pointToInfinty();

    signal segmentInfinite[2][2];
    segmentInfinite[0][0] <== point[0];
    segmentInfinite[0][1] <== point[1];
    segmentInfinite[1][0] <== extreme;
    segmentInfinite[1][1] <== point[1];

    component intersect[n];
    component collinearP[n];
    component segmentP[n];

    var sum = 0;

    for(var i = 0; i < n; i++){
        var j = i + 1;
        if(j == n){
            j = 0; // load first polygon vertex
        }
        intersect[i] = Intersects();
        intersect[i].p1[0] <== polygon[i][0];
        intersect[i].p1[1] <== polygon[i][1];
        intersect[i].q1[0] <== polygon[j][0];
        intersect[i].q1[1] <== polygon[j][1];
        intersect[i].p2[0] <== segmentInfinite[0][0];
        intersect[i].p2[1] <== segmentInfinite[0][1];
        intersect[i].q2[0] <== segmentInfinite[1][0];
        intersect[i].q2[1] <== segmentInfinite[1][1];
        sum += intersect[i].out;

        // Check if P collinear with current segment
        collinearP[i] = Orientation();
        collinearP[i].p[0] <== polygon[i][0];
        collinearP[i].p[1] <== polygon[i][1];
        collinearP[i].q[0] <== point[0];
        collinearP[i].q[1] <== point[1];
        collinearP[i].r[0] <== polygon[j][0];
        collinearP[i].r[1] <== polygon[j][1];

        segmentP[i] = OnSegment(); 
        segmentP[i].p[0] <== polygon[i][0];
        segmentP[i].p[1] <== polygon[i][1];
        segmentP[i].q[0] <== point[0];
        segmentP[i].q[1] <== point[1];
        segmentP[i].r[0] <== polygon[j][0];
        segmentP[i].r[1] <== polygon[j][1];

        var checkP = collinearP[i].out + segmentP[i].out;
        if(checkP == 4) sum += 1;
    }
    log(sum);
    // ASSERT: sum is ODD, OK to compute PROOF
    inside <-- sum % 2;
    inside === 1;
}

component main{public[polygon]} = PointInPolygon(3);