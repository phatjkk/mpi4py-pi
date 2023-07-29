import math

def simpsons_rule(a, b, n):
  h = (b - a) / n
  sum = (f(a) + f(b)) / 2
  for i in range(1, n):
    sum += 2 * f(a + i * h)
  return sum * h

def f(x):
  return math.sqrt(1 - x ** 2)

def main():
  a = 0
  b = 1
  n = 100000
  pi = simpsons_rule(a, b, n) * 4
  print("The value of pi is:", pi/2)

if __name__ == "__main__":
  main()
