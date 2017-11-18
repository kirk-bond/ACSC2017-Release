from brokenrsa import RSA
def main():
    rsa = RSA()
    with open('flag.txt', 'r') as infile:
        filedata = infile.read()
    print 'Generating keypair...'
    rsa.gen_keypair()
    print 'Done!'
    encrypted_filedata = rsa.raw_encrypt_message(filedata)
    public_key = rsa.dump_pub_key()

    with open('encrypted_flag.txt', 'w') as outfile:
        outfile.write(encrypted_filedata)

    with open('pubkey.json', 'w') as outfile:
        outfile.write(public_key)

if __name__ == '__main__':
        main()
