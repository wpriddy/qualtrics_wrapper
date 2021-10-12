#%%
import time
import getpass as gp

def convert(val) -> 'returns string int comparison':
    return (str(int(val)))

def time_taken(func) -> 'returns the time taken to run a function':

    def wrapper(*args, **kwargs):
        start = time.time()
        return_statement = func(*args, **kwargs)
        runtime = str(round(n , 2)) + ' seconds' if abs((n := time.time() - start)) < 60 else str(convert(minutes := n // 60)) + ' minutes and ' + str(convert(n - minutes * 60)) + ' seconds'

        print(f'Time Taken for "{func.__name__.title()}": {runtime}')        
        return return_statement
    return wrapper

def who(func):

    def wrapper(*args, **kwargs):
        func(*args, **kwargs)
        print('Welcome ' + gp.getuser() + '!')      

    return wrapper
# %%
