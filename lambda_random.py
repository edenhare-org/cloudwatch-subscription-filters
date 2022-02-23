import random

random.seed()

def handler(event, context):
  
  r = random.randint(0,1)
  
  if r == 0:
    print("OK")
  else:
    print("FAIL")
    
#
# for testing
#
if __name__ == "__main__":
  for x in range(0,10):
    handler({},"")
  
