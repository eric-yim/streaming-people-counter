
def iou(double x1_1, double y1_1, double x2_1, double y2_1,
        double x1_2, double y1_2, double x2_2, double y2_2):
    cdef double intersection_width
    cdef double intersection_height
    cdef double intersection_area
    cdef double box1_area
    cdef double box2_area
    cdef double union_area
    intersection_width = max(min(x2_1, x2_2) - max(x1_1, x1_2),0)
    intersection_height = max(min(y2_1, y2_2) - max(y1_1, y1_2),0)
    intersection_area = intersection_width * intersection_height
    box1_area = (x2_1 - x1_1) * (y2_1 - y1_1)
    box2_area = (x2_2 - x1_2) * (y2_2 - y1_2)
    union_area = box1_area + box2_area - intersection_area
    return intersection_area / union_area


def iou_int(int x1_1, int y1_1, int x2_1, int y2_1,
        int x1_2, int y1_2, int x2_2, int y2_2):
    cdef int intersection_width
    cdef int intersection_height
    cdef double intersection_area
    cdef int box1_area
    cdef int box2_area
    cdef double union_area
    intersection_width = max(min(x1_2, x2_2) - max(x1_1, x2_1),0)
    intersection_height = max(min(y1_2, y2_2) - max(y1_1, y2_1),0)
    intersection_area = intersection_width * intersection_height
    box1_area = (x2_1 - x1_1) * (y2_1 - y1_1)
    box2_area = (x2_2 - x1_2) * (y2_2 - y1_2)
    union_area = box1_area + box2_area - intersection_area
    return intersection_area / (union_area + 1e-5)