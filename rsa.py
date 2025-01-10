import os

def modInverse(e, phi):
    for d in range(2, phi):
        if (e * d) % phi == 1:
            return d
    return -1

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def generateKeys():
    p = 7919
    q = 1009
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 0
    for e in range(2, phi):
        if gcd(e, phi) == 1:
            break
    d = modInverse(e, phi)
    return e, d, n

def encrypt_block(block, e, n):
    return pow(block, e, n)

def decrypt_block(block, d, n):
    return pow(block, d, n)

def encrypt_file(input_file, output_file, e, n):
    block_size = (n.bit_length() - 1) // 8
    with open(input_file, 'rb') as f_in, open(output_file, 'wb') as f_out:
        while chunk := f_in.read(block_size):
            #verifica ca blocul nu e gol si citeste octeti din fisier de dim block_size
            block = int.from_bytes(chunk, byteorder='big')
            encrypted_block = encrypt_block(block, e, n)
            f_out.write(encrypted_block.to_bytes((n.bit_length() + 7) // 8, byteorder='big'))

            #+7 ca sa fac rotunjirea in sus, sa am suficienti octeti pt a repr datele
            
def decrypt_file(input_file, output_file, d, n):
    block_size = (n.bit_length() + 7) // 8
    with open(input_file, 'rb') as f_in, open(output_file, 'wb') as f_out:
        while chunk := f_in.read(block_size):
            block = int.from_bytes(chunk, byteorder='big')
            decrypted_block = decrypt_block(block, d, n)
            f_out.write(decrypted_block.to_bytes((block.bit_length() + 7) // 8, byteorder='big').rstrip(b'\x00'))
