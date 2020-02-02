import sys
import math
#import time


def get_input():
	input = sys.stdin.readline()
	M, x2, x3 = input.split(" ")
	return int(M), int(x2), int(x3)


def coprime(a, b):
	return math.gcd(a, b) == 1


def egcd(a,b):
	x0, x1 = 0,1
	while a!=0:
		q,b,a = b//a,a,b%a
		x0,x1=x1,x0-q*x1
	return x0


def solve(gen):
	A,C = gen
	return (egcd(A,M)*(x2 - C))%M

def get_output(gens):
	out = list(map(solve, gens))
	#min_ = min(out)
	#max_ = max(out)
	#count = len(out)
	#return count, min_, max_
	return len(out), min(out), max(out)

def get_prime_factors(a):
	p = 2
	factors = set()
	add = factors.add
	while a >= p:
		if a%p == 0:
			a = a/p
			add(p)
		else:
			p += 1
	return list(factors)


def filter_possible_gens(M):
	list_of_M = get_prime_factors(M)
	product = 1
	for i in list_of_M:
		product *= i

	if M % 4 == 0:
		if product > 4:
			if product%4 == 0:
				list_of_a = [i for i in range(product + 1, M, product)]
			elif product%4 == 1:
				list_of_a = [i for i in range(4*product + 1, M, product*4)]
			elif product%4 == 2:
				list_of_a = [i for i in range(2*product + 1, M, product*2)]
			else:
				list_of_a = [i for i in range(4*product + 1, M, product*4)]
		else:
			list_of_a = [i for i in range(5, M, 4)]
	else:
		list_of_a = [i for i in range(product+1, M, product)]
	gens = map(fast_function, list_of_a)
	return gens


def fast_function(a):
	#y = ((a * x2) % M)
	#c = ((x3 - ((a * x2) % M)) % M)
	return a,((x3 - ((a * x2) % M)) % M)


if __name__ == "__main__":
	#start = time.time()
	M, x2, x3 = get_input()
	possible_gens = filter_possible_gens(M)
	result = get_output(possible_gens)
	print("{} {} {}".format(result[0], result[1], result[2]))
	#end = time.time()
	#print(end-start)