from math import sqrt
from random import randint
from sympy import randprime
from Crypto.Random import get_random_bytes
from entities_pip import Polygon, Prover, Verifier

'''
Generate a prime P, given a specific range in Integers
'''
def aPrime(initial: int, final: int):
    return randprime(initial, final) # Between 0 and 19

'''
Generate a number of the field Zp: Integer between 1 and (p-1), where p is a Prime.
'''
def randomZp(p: int):
    return randint(1, p-1)

# Execute ZKP 
def zkpPIP(prover: Prover, verifier: Verifier) -> bool:
    # Generic Variables Setup

    # Witness Phase: 
        # Prover computes Y, sends it to verifier
    y = prover.proof()
    verifier.setReceivedValue(y) # y: verifier.received[0] 
    print(f"--- (Witness Phase) ---\n {prover.getName()}  computes: \n Y: {y}")
    print(f"\n ...sends Y to {verifier.getName()} ...")

    prover.chooseR()
    c = prover.cStatement()
    verifier.setReceivedValue(c) # c: verifier.received[1]
    print(f"{prover.getName()}  computes: \n C: {c}")
    print(f"\n ...sends C to {verifier.getName()} ...")

    # Challenge Phase:
        # Verifier randomly chooses between 0 and 1, sends it to the Prover
    verifier.challenge()
        # Prover computes a statement based on the challenge
    challengeSt = prover.challengeStatement(verifier.getChallenge())
    verifier.setReceivedValue(challengeSt) # challengeSt: verifier.received[2]
    print(f"{prover.getName()}  computes: \n statementFromChallenge: {challengeSt}")
    print(f"\n ...sends statement to {verifier.getName()} ...")

    return verifier.verify()

'''
Setup a verification zkpPIP process between two entities.
'''
if __name__ == '__main__': 
    # --- PROMPT INTRO ---
    print("----------------------------------- \n-----( ZKP Point In Polygon )------ \n----------------------------------- \nCopyright @Bitrath\n")

    # --- SETUP ZKP ---
        # Generate a random modulo m
    prime = aPrime(0, 20) # Between 0 and 19

        # Obtain a generator of the multiplicative field Zp
    generator = randomZp(prime)

        # Generate a Polygon
    polygon = Polygon(3) # Triangle
    polygon.addPoint((1,1))
    polygon.addPoint((3,4))
    polygon.addPoint((5,1))
    print(polygon.__str__())

    point = (3,2)

        # Create Prover
    address_p = get_random_bytes(16)
    name_p = "Bob"
    #Bob = Prover(address_p, name_p, prime, generator, polygon, point)
    Bob = Prover(address_p, name_p, 11, 4, polygon, point)
    #print(Bob.__str__())

        # Create Verifier
    address_v = get_random_bytes(16)
    name_v = "Alice"
    #Alice = Verifier(address_v, name_v, prime, generator, polygon, point)
    Alice = Verifier(address_v, name_v, 11, 4, polygon, point)
    #print(Alice.__str__())

        # Prover checks if it has a point into common polygon
        # Then, computes a secret
    if not Bob.pointInsidePolygon(): 
        Bob.computeX()
        print(f"\nBob - OUTSIDE - X:{Bob.getSecret()}")
    else: 
        Bob.computeX()
        print(f"\nBob - INSIDE - X: {Bob.getSecret()}")

        # Verifier also computes a secret
    Alice.computeX()
    print("Alice X:", Alice.getSecret())

        # Prompt SETUP styling
    print("\n*** SETUP ***\n")
    print(f"{Bob.getName()} wants to prove to {Alice.getName()} that he knows the ccordinate of a point inside a common polygon.")
    print(f"They aggre on common parameteres, such as:\n-Prime: {prime}\n-Generator: {generator}\n-Polygon: {polygon.__str__()}\n")

        # --- RUN ZKP ---
    print("\n*** ZKP ALGORITHM ***\n")
        # run zkpPIP
    result = zkpPIP(Bob, Alice)

        # --- RESULTS PRINT ---
    print(f"\n*** RESULTS *** \nDoes {Bob.getName()} really know the secret? \n({Alice.getName()} says) {result}\n")
    print(f"\n*** ENTITIES *** {Bob.__str__()} \n {Alice.__str__()}")
