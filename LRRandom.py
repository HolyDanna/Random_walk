# Just a small function to be able to know if the m we'll use is prime or not
def isprime(n):
    n = abs(int(n))
    if n < 2:
        return False
    if n == 2:
        return True
    if not n & 1:
        return False
    for x in range(3, int(n**0.5)+1, 2):
        if n % x == 0:
            return False
    return True


class LRR(object):
    def __init__(self, m = 2**31-1, a1 = 784588716, a2 = 163490618 , x1=897, x2 = 12461):
        # It is possible to change the default values by specifying the values
        # for the parameters
        # note that if the given m value is not prime, we'll use the prime number
        # 2^31-1
        # The values of the parameters are also kept below the value of m
        super(LRR, self).__init__()
        if isprime(m):
            self.m = m
        else:
            self.m = 2**31-1
        self.a1 = a1 % self.m
        if self.a1 == 0 or self.a1 == 1:
            self.a1 = 784588716
        self.a2 = a2 % self.m
        if self.a2 == 0 or self.a2 == 1:
            self.a2 = 163490618
        self.x1 = x1 % self.m
        self.x2 = x2 % self.m
        if self.x1 == 0 and self.x2 == 0:
            self.x2 = 897
        # We do not check if the number will be too high as Python does not have
        # a defined MAX_INT value, thus not creating problem in the a*z multiplication

    # returns a random number between 0 and 1 (strictly different from both)
    def rand(self):
        new_x = (self.x1*self.a2 + self.x2*self.a1) % self.m
        self.x1 = self.x2
        self.x2 = new_x
        return new_x/self.m

    # returns a random integer between 0 and i-1
    def randint(self, i):
        new_x = (self.x1*self.a2 + self.x2*self.a1) % self.m
        self.x1 = self.x2
        self.x2 = new_x
        return int(new_x*i/self.m)
