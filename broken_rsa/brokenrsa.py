#All code above the line marked UNSAFE can be considered trusted
import random
import json
smallprimes = [2]

#Only print messages when being verbose
def log(msg, verbose = True):
    if verbose:
        print msg


#Performs modular exponentiation
#Suitable for large numbers
#Same as (a ** b) % n
def modexp(a, b, n):
    if a == 0:
        return 0
    accumulator = a
    result = 1 % n
    while b > 0:
        if b & 0x1:
            result = (result * accumulator) % n
        accumulator = (accumulator * accumulator) % n
        b >>= 1
    return result

#Fill our global list of small primes
def fill_smallprimes():
    global smallprimes
    i = 3
    upper_limit = 1000
    while i < upper_limit:
        is_prime = True
        for p in smallprimes:
            if i % p == 0:
                is_prime = False
                break
        if is_prime:
            smallprimes.append(i)
        i += 2

#Returns a number garunteed to have n bits
#n must be a multiple of 8
def get_n_bit_number(n):
    num_bytes = n / 8
    rng = random.SystemRandom()
    result = rng.getrandbits(n)
    #set the high bit to garuntee size
    result |= 1 << (n - 1)
    return result

#Returns an n bit probably prime number
#n must be a multiple of 8
def get_n_bit_probable_prime(n):
    current = get_n_bit_number(n)
    current |= 1
    tries = 0
    while not is_probably_prime(current):
        current += 2
        tries += 1
    return current

#Returns true if n is probably prime
#        false if in is definitely not prime
def is_probably_prime(n):
    for p in smallprimes:
        if n % p == 0:
            return False

    return miller_rabin(n, 25)
    

#Performs k rounds of miller-rabin
#compositeness tests on n
#Returns true if n is probably prime
#        false if n is definitly not prime
def miller_rabin(n, k):
    #input must be odd
    if n % 2 == 0:
        return False
    #write n - 1 as (2 ** s) * d
    d = n - 1
    s = 0
    while d % 2 == 0:
        s += 1
        d /= 2
    for i in range(k):
        a = random.randint(2, n - 1)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        passed_round = False
        for r in xrange(1, s):
            x = pow(x, 2, n)
            if x == 1:
                return False
            if x == (n - 1):
                passed_round = True
                break
        if not passed_round:
            return False
    return True

#excercises prime prime generation    
def test_prime_gen(verbose):
    log('Generating 512 bit prime', verbose)
    p = get_n_bit_probable_prime(512)
    log('p = %d' % p, verbose)
    return True


#Taken from rosetta code
#Returns (g, x, y)
#such that (x * aa) + (bb * y) = g    
def extended_gcd(aa, bb):
    lastremainder, remainder = abs(aa), abs(bb)
    x, lastx, y, lasty = 0, 1, 1, 0
    while remainder:
        lastremainder, (quotient, remainder) = remainder, divmod(lastremainder, remainder)
        x, lastx = lastx - quotient*x, x
        y, lasty = lasty - quotient*y, y
    return lastremainder, lastx * (-1 if aa < 0 else 1), lasty * (-1 if bb < 0 else 1)

#Calculates modular inverse of a over m
#Returns b such that
# (a * b) % m == 1
#if a and m are not co-prime no modular inverse exists and raises an exception
def modinv(a, m):
    g, x, y = extended_gcd(a, m)
    if g != 1:
        raise ValueError('%d and %d are not co-prime' % (a, m))
    return x % m

#Convert an arbitrary ascii string to a number
#using ascii values directly
def str_to_num(data):
    result = 0
    for c in data:
        result <<= 8
        result += ord(c)
    return result

#Convert a number to an anscii string using
#ascii values directly
def num_to_str(num, min_size=0):
    result = ''
    while num != 0:
        result = chr(num & 0xff) + result
        num >>= 8
    if len(result) < min_size:
        result = ('\x00' * (min_size - len(result))) + result
    return result

#Test conversion from string to number and back
def test_str_num_conversion(verbose):
    test_str = 'This is a test string'
    expected = test_str
    num = str_to_num(test_str)
    actual = num_to_str(num)
    print 'Testing string to number conversion...'
    print 'Input:  %s' % test_str
    print 'Number: %d' % num
    print 'Output: %s' % actual
    passed = False
    if expected == actual:
        passed = True
    print 'Passed: %s' % passed
    return passed 
# Test math with values small enough to check by hand
def test_small_rsa(verbose):
    has_failed = False
    log('Testing rsa with small numbers')
    p = 47
    q = 71
    e = 79
    m = 688
    c = 1570
    rsa = RSA(p, q, e)
    log('Encrypting %d' % m, verbose)
    expected = c
    actual = rsa.raw_encrypt_num(m)
    log('Expected: %d' % expected)
    log('Actual:   %d' % actual)
    if expected != actual:
        has_failed = True
        print 'FAIL: Expected != actual'
    log('Decrypting %d' % c)
    expected = m
    actual = rsa.raw_decrypt_num(c)
    log('Expected: %d' % expected)
    log('Actual:   %d' % actual)
    if expected != actual:
        has_failed = True
        print 'FAIL: Expected != actual'
    return not has_failed

# Test math with ascii message
def test_rsa_message(verbose):
    log('Testing rsa with text', verbose)
    message = 'Test message'
    rsa = RSA()
    rsa.gen_keypair()
    ct = rsa.raw_encrypt_message(message)
    expected = message
    actual = rsa.raw_decrypt_ciphertext(ct)
    log('Expected: %s' % expected, verbose)
    log('Actual:   %s' % actual, verbose)
    if expected != actual:
        log('Fail', verbose)
        return False
    return True

# Test serialization and deserialization produces working instances
def test_rsa_serialization(verbose):
    log('Testing rsa serialization', verbose)
    message = 'Test message'
    rsa = RSA()
    rsa.gen_keypair()
    pubkey_json = rsa.dump_pub_key()
    log('Public key: %s' % pubkey_json)
    prikey_json = rsa.dump_priv_key()
    log('Private key: %s' % prikey_json)
    encryptor = RSA()
    encryptor.load_json(pubkey_json)
    decryptor = RSA()
    decryptor.load_json(prikey_json)
    ct = encryptor.raw_encrypt_message(message)
    expected = message
    actual = decryptor.raw_decrypt_ciphertext(ct)
    log('Expected: %s' % expected, verbose)
    log('Actual:   %s' % actual, verbose)
    if expected != actual:
        log('Fail', verbose)
        return False
    
    return True

# Perform a self test of the library and throw an exception if
# any tests faile
# verbose - will print to screen if true
def self_test(verbose):
    log('Performing self tests', verbose)
    has_failed = False
    tests= [
            test_prime_gen,
            test_str_num_conversion,
            test_small_rsa,
            test_rsa_message,
            test_rsa_serialization,
            ]
    for test in tests:
        test_name = str(test)
        result = test(verbose)
        if not result:
            has_failed = True
        log('%s Passed = %s' % (test_name, result))
        if has_failed:
            raise Exception('Self tests failed')

# Perform library initialization
def init_library():
    fill_smallprimes()
    verbose = False
    if __name__ == '__main__':
        verbose = True
#    self_test(verbose)


#############################################
## All UNSAFE code is below this line      ##
#############################################


#Class for performing RSA encryption and decryption
class RSA:
    def __init__(self, p = None, q = None, e = None):
        self.p = p
        self.q = q
        self.n = None
        if p is not None and q is not None:
            self.n = p * q
        self.e = e
        if e is not None and self.n is not None:
            phi_of_p = p - 1
            phi_of_q = q - 1
            phi_of_n = phi_of_p * phi_of_q
            self.d = modinv(self.e, phi_of_n)

    # Generate a new keypair
    def gen_keypair(self):
        # private: prime1     
        self.p = get_n_bit_probable_prime(2048)
        # private: prime2
        self.q = get_n_bit_probable_prime(2048)
        # publice: public modulus
        self.n = self.p * self.q
        
        # private: count of numbers less than prime1 relatively prime to it
        phi_of_p = self.p - 1
        # private: count of numbers less than prime2 relatively prime to it
        phi_of_q = self.q - 1
        # private: count of numbers less than public modulus relatively prime to it
        phi_of_n = phi_of_p * phi_of_q
        # public: encryption exponent
        self.e = 65537
        # private: decryption exponent
        self.d = modinv(self.e, phi_of_n)

    # Perform bounds checked raw encryption on num
    def raw_encrypt_num(self, m):
        if m > self.n:
            raise Exception('Number to encrypt is too big')
        c = pow(m, self.e, self.n)
        return c

    # Convert message to number encrypt and return result as string
    def raw_encrypt_message(self, message):
        m = str_to_num(message)
        c = self.raw_encrypt_num(m)
        ciphertext = num_to_str(c)
        return ciphertext
        
    # Perform bounds checked raw decryption on num
    def raw_decrypt_num(self, c):
        if c > self.n:
            raise Exception('Number to decrypt is too big')
        m = pow(c, self.d, self.n)
        return m
            
    # Convert ciphertext to a number decrypt and return result as string
    def raw_decrypt_ciphertext(self, ciphertext, min_size = 0):
        c = str_to_num(ciphertext)
        m = self.raw_decrypt_num(c)
        message = num_to_str(m, min_size)
        return message

    # Dump the public key as a json blob
    def dump_pub_key(self):
        key_dict = {
                    'n' : self.n,
                    'e' : self.e,
                    'p' : self.p
                   }
        return json.dumps(key_dict)

    # Dump the private key as a json blob
    def dump_priv_key(self):
        key_dict = {
                    'n' : self.n,
                    'e' : self.e,
                    'd' : self.d,
                    }
        return json.dumps(key_dict)

    # Initialize cryptovariables from json blob
    def load_json(self, json_blob):
        self.p = None
        self.q = None
        self.n = None
        self.e = None
        self.d = None
        key_dict = json.loads(json_blob)
        for key in key_dict:
            setattr(self, key, key_dict[key])

init_library()
    
