from __future__ import print_function
cdef class TrackedObject:
    cdef int idx
    cdef double[4] box
    cdef int unused_count
    cdef double[2] start_centroid
    cdef double[2] current_centroid
    cdef bint has_crossed
    cdef int reset_threshold
    cdef direction
    cdef int cross_count
    def __init__(self,idx,box,reset_threshold=60):
        self.idx = idx
        self.box = box
        self.unused_count = 0
        self.start_centroid = [(box[0]+box[2])/2,(box[1]+box[3])/2]#x,y
        self.current_centroid = [(box[0]+box[2])/2,(box[1]+box[3])/2]
        self.has_crossed = False
        self.direction = ''
        self.reset_threshold = reset_threshold
        self.cross_count = 0

    def update(self,box):
        self.box = box
        self.unused_count = 0
        self.current_centroid = [(box[0]+box[2])/2,(box[1]+box[3])/2]#x,y
        if self.has_crossed:
            self.cross_count+=1
            if self.cross_count>=self.reset_threshold:
                self.has_crossed=False
                self.start_centroid = [(box[0]+box[2])/2,(box[1]+box[3])/2]#x,y
    def unused(self):
        self.unused_count+=1
    def get_has_crossed(self):
        return self.has_crossed
    def mark_crossed(self):
        self.has_crossed = True
        self.cross_count = 0
        self.up_or_down()
    def up_or_down(self):
        y0 = self.start_centroid[1]
        y1 = self.current_centroid[1]
        self.direction='up'
        if y1>y0:
            self.direction = 'down'

    
    def get_unused_count(self):
        return self.unused_count
    def get_direction(self):
        return self.direction
    def get_box(self):
        return self.box
    def get_idx(self):
        return self.idx
    def get_has_crossed(self):
        return self.has_crossed
    def get_start_centroid(self):
        return self.start_centroid
    def get_current_centroid(self):
        return self.current_centroid
    def get_cross_count(self):
        return self.cross_count