import random
from dataclasses import dataclass
from enum import Enum
from typing import List, Tuple

class Basis(Enum):
    RECTILINEAR = '+'  # For 0° and 90° measurements
    DIAGONAL = 'x'     # For 45° and 135° measurements

class Bit(Enum):
    ZERO = '0'
    ONE = '1'

@dataclass
class Qubit:
    bit: Bit
    basis: Basis
    
def generate_random_bits(n: int) -> List[Bit]:
    """Generate n random classical bits."""
    return [random.choice(list(Bit)) for _ in range(n)]

def generate_random_bases(n: int) -> List[Basis]:
    """Generate n random measurement bases."""
    return [random.choice(list(Basis)) for _ in range(n)]

def measure_qubit(qubit: Qubit, measurement_basis: Basis) -> Bit:
    """
    Measure a qubit using the given basis.
    Returns random result if bases don't match (quantum uncertainty).
    """
    if measurement_basis == qubit.basis:
        return qubit.bit
    return random.choice(list(Bit))

def bb84_protocol(n_bits: int) -> Tuple[str, float]:
    """
    Simulate the BB84 quantum key distribution protocol.
    Returns the shared key and the theoretical security level.
    """
    # Alice's preparation
    alice_bits = generate_random_bits(n_bits)
    alice_bases = generate_random_bases(n_bits)
    qubits = [Qubit(bit, basis) for bit, basis in zip(alice_bits, alice_bases)]
    
    # Bob's measurement
    bob_bases = generate_random_bases(n_bits)
    bob_measurements = [measure_qubit(qubit, basis) 
                       for qubit, basis in zip(qubits, bob_bases)]
    
    # Base comparison and key sifting
    matching_bases = [i for i in range(n_bits) 
                     if alice_bases[i] == bob_bases[i]]
    
    # Generate final key from matching bases
    key = ''.join(alice_bits[i].value for i in matching_bases)
    
    # Calculate theoretical security level
    security_level = 1 - (0.75 ** len(key))  # Probability of detecting eavesdropping
    
    return key, security_level

def demonstrate_protocol():
    """Demonstrate the BB84 protocol with a small example."""
    n_bits = 20
    key, security = bb84_protocol(n_bits)
    
    print(f"Generated quantum-secured key: {key}")
    print(f"Key length: {len(key)} bits")
    print(f"Theoretical security level: {security:.2%}")
    print("\nThis key can now be used for symmetric encryption of messages.")

if __name__ == "__main__":
    demonstrate_protocol()
