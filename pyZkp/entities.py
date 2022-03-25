from random import randint
from math import sqrt

'''
 Entity: a basic communication entity
'''
class Entity:
    # Has an address, a prime, a secret and a statement
    # --> consider passing an encrypted secret at init
    def __init__(self, a, n, m: int):
        self._address = a
        self._name = n
        self._modulo = m
        self._secret = None
        self._statement = None

    def __str__(self):
        return '\nEntity (' + str(self._name) + '):' + '\n--address: ' + str(self._address) + '\n--modulo: ' + str(self._modulo) + '\n--secret: ' + str(self._secret) + '\n--statement: ' + str(self._statement) + '\n'

    # --- GETTERS ---
    # Get Address
    def getAddress(self):
        return self._address

    # Get Name
    def getName(self):
        return self._name

    # Get Prime
    def getModulo(self):
        return self._modulo

    # Get Secret (USED FOR TESTING)
    def getSecret(self):
        return self._secret 

    # Get Statement
    def getStatement(self):
        return self._statement

    # --- SETTERS ---
    # Set Address
    def setAddress(self, ad):
        self._address = ad

    # Set Name 
    def setName(self, nn):
        self._name = nn

    # Set Modulo
    def setModulo(self, mod):
        self._modulo = mod

    # Set Secret USED FOR TESTING
    def setSecret(self, s):
        self._secret = s

    # Set Statement
    def setStatement(self, st):
        self._statement = st

    # --- METHODS ---
    # Generate a random secret
    def setRandomSecret(self):
        # self.prime is not yet set, return
        self._secret = randint(int(sqrt(self._modulo)), self._modulo - 1) # Between sqrt(n) and n-1

    # Set a statement from a personal secret
    def setStatememtFromSecret(self):
        self._statement = pow(self._secret, 2) % self._modulo # v = (s^2) modn

'''
Prover: an Entity that can compute a proof
'''
class Prover(Entity):
    def __init__(self, a, n, p: int):
        super().__init__(a, n, p)
        self._personalStatement = None

    def __str__(self):
        return '\nProver (' + str(self._name) + '):' + '\n--address: ' + str(self._address) + '\n--modulo: ' + str(self._modulo) + '\n--secret: ' + str(self._secret) + '\n--v statement: ' + str(self._statement) + '\n--r statement: ' + str(self._personalStatement) + '\n'

    # --- GETTERS Prover ---
    # Get Personal Statement
    def getPersonalStatement(self):
        return self._personalStatement

    # --- SETTERS Prover ---
    #Set a personal statement, the verifier won't be able to.
    def setPersonalStatement(self):
        self._personalStatement = randint(1, self._modulo - 1)

    # --- METHODS Prover ---
    # Compute a send-statement
    def computeSendStatement(self):
        if self._personalStatement == None : self.setPersonalStatement()
        return pow(self._personalStatement, 2) % self._modulo # x = (r^2) modn

    # Compute a Proof from a challenge
    def proof(self, a):
        if a == 0:
            return self._personalStatement                                     # proof = r
        elif a == 1:
            return (self._personalStatement * self._secret)%(self._modulo)   # proof = (r*s) modn


'''
Verifier: an Entity that can verify a proof
'''
class Verifier(Entity):
    def __init__(self, a, n, p: int):
        super().__init__(a, n, p)

    def __str__(self):
        return '\nVerifier (' + str(self._name) + '):' + '\n--address: ' + str(self._address) + '\n--modulo: ' + str(self._modulo) + '\n--secret: ' + str(self._secret) + '\n--v statement: ' + str(self._statement) + '\n'

    # --- GETTERS Verifier ---
    # --- SETTERS Verifier ---

    # --- METHODS Verifier ---
    # Challenge assigner
    def challenge(self):
        return randint(0, 1)

    # Verifies a proof received
    def verify(self, proof, x, a):
        received = pow(proof, 2) % self._modulo # (proof^2) modn
        if a == 0:
            # x [the Prover could trick the Verifier]
            personal = x
        elif a == 1: 
            # (x)*(v^a) modn [the Prover cannot trick the Verifier]
            personal = (x * (pow(self._statement,a))) % self._modulo 
        print("\n--- (Verification Phase) ---\n " + self.getName() + " computes:\n * Statement from Proof -> "+ str(received) + "\n * Personal statement based on the challenge -> " + str(personal))

        # validation
        if received == personal: return True # proof^2 == x*(v^a) modn
        return False