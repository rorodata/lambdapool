def fibonacci(n):
    '''A naive implementation of computing n'th fibonacci number
    '''
    if n==0: return 0
    if n==1: return 1
    return fibonacci(n-1) + fibonacci(n-2)

def factorial(n):
    '''Returns factorial of a number
    '''
    if n<0: raise ValueError('Factorial of a negative number does not exist')
    if n==0: return 1
    return n*factorial(n-1)
