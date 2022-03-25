from math import sqrt
from random import randint
from sympy import randprime
from Crypto.Random import get_random_bytes
from entities import Prover, Verifier

'''
Generate n = p*q from two large private primes
'''
def generateModulo():
    p = randprime(0, 20) # Between 0 and 19
    q = randprime(0, 20) # Between 0 and 19
    return p*q

'''
Generate two random secrets
'''
def generateSecrets(p: Prover, v: Verifier, same: bool):
    if same :
        # Generates an equal secret to both
        s = randint(int(sqrt(p.getModulo())), v.getModulo() - 1)
        p.setSecret(s)
        v.setSecret(s)
        return 
    p.setRandomSecret()
    v.setRandomSecret()

'''
Execute a zkp verification algorithm.
- p: Prover
- v: Verifier
'''
def zero_knowledge_proof(p: Prover, v: Verifier):
    # Witness Phase: 
        # Prover computes V & X, sends X to the Verifier
    p.setStatememtFromSecret() # V, Prover
    x = p.computeSendStatement() # X
    print("--- (Witness Phase) ---\n " + p.getName() + " computes: \n v = " + str(p.getPersonalStatement()) + "\n x = " + str(x))
    print("\n ...sends x to " + v.getName() + "...")

    # Challenge Phase:
        # Verifier randomly chooses between 0 and 1, sends it to the Prover
    alpha = v.challenge()
    print("\n--- (Challenge Phase) ---\n " + v.getName() + " chooses the challenge: " + str(alpha))
    print("\n ...sends the challenge to " + p.getName() + "...")

    # Response Phase:
        # Prover computes a Proof from the Challenge received, sends the result to the Verifer
    phi = p.proof(alpha)
    print("\n--- (Response Phase) ---\n" + p.getName() + " computes the proof: " + str(phi))
    print("\n ...sends the proof to " + v.getName() + "...")

    # Verification Phase:
        # Verifier validates the Proof, takes a decision
    v.setStatememtFromSecret() # V, Verifier
    validation = v.verify(phi, x, alpha)
    print("\n" + v.getName() + " validates the proof as " + str(validation) + "\n")

    return validation


'''
Setup a verification zkp process between two entities.
'''
def main():
    # --- PROMPT INTRO ---
    print("------------------ \n----- Z K P ------ \n------------------ \nCopyright @Bitrath\n")

    # --- SETUP ZKP ---
        # Generate a random modulo m
    m = generateModulo() # Between 0 and 19

        # Create Prover
    address_p = get_random_bytes(16)
    name_p = "Bob"
    pr = Prover(address_p, name_p, m)

        # Create Verifier
    address_v = get_random_bytes(16)
    name_v = "Alice"
    vr = Verifier(address_v, name_v, m)

        # Set random secrets to Verify
    generateSecrets(pr, vr, False)

        # Prompt setupm styling
    print("*** SETUP ***\n")
    print(str(pr.getName()) + " wants to prove to " + str(vr.getName()) + " that he knows a certain secret number.\n")
    print("They decide that the shared modulo used by their algorithms will be: ", m)

    # --- RUN ZKP ---
    print("\n*** ZKP ALGORITHM ***\n")

        # Call Verification Algorithm
    result = zero_knowledge_proof(pr, vr)

    # --- RESULTS PRINT ---
    print("\n*** RESULTS *** \n Does " + pr.getName() + " really know the secret? \n(" + vr.getName() + " says) " + str(result) + "\n")
    print("\n*** ENTITIES *** " + pr.__str__() + vr.__str__())

main()