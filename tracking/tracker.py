from tracking.iou import iou
from tracking.tracked_object import TrackedObject

class Tracker:
    def __init__(self,unused_threshold=10,printout=False,object_reset_threshold=100):
        self.objects = []
        self.count = 0
        self.unused_threshold = unused_threshold
        self.printout = printout
        self.object_reset_threshold=object_reset_threshold

    def track(self,new_boxes):
        old_boxes = [obj.get_box() for obj in self.objects]
        #old_unmatched = []
        remove_oboxes = [False for _ in old_boxes]
        used_boxes = [False for _ in new_boxes]
        matched = []
        for o,obox in enumerate(old_boxes):
            #greedy
            ious = [self.iou(obox,nbox,ubox) for nbox,ubox in zip(new_boxes,used_boxes)]
            #print(ious)
            idx = self.max_idx(ious)
            
            if idx is None:
                #old_unmatched.append(self.objects[o])
                self.objects[o].unused()
                #print(ious,idx,self.objects[o].unused_count)
                 # remove lingering boxes
                if self.objects[o].get_unused_count() >= self.unused_threshold:
                    remove_oboxes[o]=True
            else:
                used_boxes[idx]=True
                self.objects[o].update(new_boxes[idx])

        # remove lingering boxes
        self.objects = [obj for obj,rbox in zip(self.objects,remove_oboxes) if not rbox]

        temp = len(self.objects)
        # unmatched new boxes
        for nbox,ubox in zip(new_boxes,used_boxes):
            if not ubox:
                self.objects.append(TrackedObject(self.count,nbox,reset_threshold=self.object_reset_threshold))
                self.count+=1
        if self.printout:
            
            info = {
                "OldBoxes": len(remove_oboxes),
                "RemovedBoxes": sum(remove_oboxes),
                "Matches": sum(used_boxes),
                "NewBoxes": len(new_boxes),
                "NewBoxesAppended":len(self.objects)-temp,
                "Total": len(self.objects)
            }
            for k,v in info.items():
                print(f"{k}:{v}")
            print('='*40)

       

        



        
    def iou(self,obox,nbox,ubox):
        if ubox:
            return 0
        return iou(*obox,*nbox)

    def max_idx(self,my_list):
        # only positive numbers for my_list
        best = 1e-5
        best_idx = None
        for idx,item in enumerate(my_list):
            if item > best:
                best=item
                best_idx = idx
        return best_idx
    def get_objects(self):
        return self.objects
