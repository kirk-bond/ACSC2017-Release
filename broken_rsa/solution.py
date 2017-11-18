from brokenrsa import RSA
from brokenrsa import modinv
def main():
    with open('encrypted_flag.txt', 'r') as infile:
        encrypted_flag = infile.read()

    with open('pubkey.json', 'r') as infile:
        pubkey = infile.read()
    rsa = RSA()
    rsa.load_json(pubkey)
####################################################
### This is where you should start your solution ###
####################################################    
    rsa.q = rsa.n / rsa.p
    phi_of_p = rsa.p - 1
    phi_of_q = rsa.q - 1
    phi_of_n = phi_of_p * phi_of_q
    rsa.d = modinv(rsa.e, phi_of_n)


####################################################
### This is where you should end your solution   ###
####################################################    
    if rsa.d is None:
        print 'RSA instance has no decryption exponent.'
        print 'You need to find d'
        return
    print 'Your flag is: %s' % rsa.raw_decrypt_ciphertext(encrypted_flag)
if __name__ == '__main__':
        main()
