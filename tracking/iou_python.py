def iou(x1_1, y1_1, x2_1, y2_1,x1_2, y1_2, x2_2, y2_2):
        intersection_width = max(min(x1_2, x2_2) - max(x1_1, x2_1),0)
        intersection_height = max(min(y1_2, y2_2) - max(y1_1, y2_1),0)
        intersection_area = intersection_width * intersection_height
        box1_area = (x2_1 - x1_1) * (y2_1 - y1_1)
        box2_area = (x2_2 - x1_2) * (y2_2 - y1_2)
        union_area = box1_area + box2_area - intersection_area
        return intersection_area / union_area