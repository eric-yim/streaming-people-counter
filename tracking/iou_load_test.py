import time
class Timer:
    def __init__(self):
        pass
    def tic(self):
        self.start = time.time()
    def toc(self):
        return time.time()-self.start
from iou import iou
import random
def generate_test_point():
    p1 = [random.random(),random.random()]
    p2 = [p1[0]+random.random(),p1[1]+random.random()]
    return p1 + p2
def test():
    t = Timer()
    total = 0.0

    for _ in range (90000):
        box1 = generate_test_point()
        box2 = generate_test_point()
        t.tic()
        result = iou(*box1,*box2)
        total+= t.toc()
    
    print(f"Time: {total}")
if __name__=='__main__':
    test()