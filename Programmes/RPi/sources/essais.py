class Test():
    def __init__(self, x=0, external=None, **args):
        external(**args)
     
def toto(z,y):
    print("ok") 
      
Test(x=0, y=0, z=0, external=toto)