HW_RATIO_MIN = 1.5
def filter_boxes(boxes):
    return [box for box in boxes if check(*box)]

def check(x0,y0,x1,y1):
    area = (y1-y0) * (x1-x0)
    y = (y0+y1)/2
    # This is a custom box size filter which is tuned to specific location
    # It is commented out because you may be running on a different location
    # if area > max_line(y):
    #     return False
    # if area < min_line(y):
    #     return False
    hw_ratio = (y1-y0)/(x1-x0)
    if hw_ratio < HW_RATIO_MIN:
        return False
    return True


def max_line(y):
    return 800 + (y*8.5)
def min_line(y):
    return -1800 + (y*6)