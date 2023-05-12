import cv2
import mmcv
from mmcv.transforms import Compose
from mmengine.utils import track_iter_progress
from mmdet.registry import VISUALIZERS
from mmdet.apis import init_detector, inference_detector
from tracking.tracker import Tracker
from utils.colors import COLORS
from utils.counter import Counter
from utils.aggregator import Aggregator
from utils.stream_reader import StreamReader
import argparse
import os
import numpy as np
from postprocessing.filter_boxes import filter_boxes
import random
parser = argparse.ArgumentParser(description='Command line arguments')

parser.add_argument('--config', '-cfg', 
    default='work_dirs/faster-rcnn_r50-caffe_fpn_ms-1x_coco-person/faster-rcnn_r50-caffe_fpn_ms-1x_coco-person.py',
    help='name of config file')
parser.add_argument('--checkpoint', '-ckpt',
    default='work_dirs/faster-rcnn_r50-caffe_fpn_ms-1x_coco-person/epoch_{}.pth',
    help='name of config')
parser.add_argument('--epoch', '-e',
    default='24',
    help='input')
parser.add_argument('--sample', '-s',
    default='sample2.png',
    help='input')
parser.add_argument('--input', '-i',
    default='https://www.youtube.com/watch?v=RQA5RcIZlAM',
    help='input')
parser.add_argument('--interval', '-int',
    default='3',
    type=int,
    help='input')
parser.add_argument('--cross', 
    default='[[260,540],[1620,740]]',
    type=eval,
    help='input')
parser.add_argument('--crop', 
    default='[0,1080,500,1920]',
    type=eval,
    help='input')
# Add a flag argument
parser.add_argument('--single', dest='single',action='store_true',
    help='single image inference')
# Parse the command-line arguments
args = parser.parse_args()

VIDEO='video'
import time
class Timer:
    def __init__(self):
        pass
    def tic(self):
        self.start = time.time()
    def toc(self):
        return time.time()-self.start
class SubTimer:
    def __init__(self):
        self.info = {}
    def tic(self):
        self.start = time.time()
    def toc(self,name):
        if not name in self.info:
            self.info[name]=time.time()-self.start
        else:
            self.info[name]+=time.time()-self.start
        self.tic()
    def get_info(self):
        return self.info
class BoxStore:
    def __init__(self):
        self.all_boxes = {}
        self.dir = 'boxes'
        os.makedirs(self.dir,exist_ok=True)
    def save_boxes(self,i,boxes):
        name = str(i).zfill(5) +'.npy'
        np.save(os.path.join(self.dir,name),np.array(boxes)) 
def visualize_line(im,cross):
    """
    Draws a line on the image
    """
    tl,br = cross
    return cv2.line(im,tl,br,[0,255,0],2)
def visualize_tracker(im,tracker):
    """
    Visualizes what the tracker is doing
    This code is tied to the variables seen in tracker.py 
    """
    for obj in tracker.get_objects():
        # If a tracked object is not found on current frame, don't display its box
        if obj.get_unused_count()>1:
            continue

        # If an object has crossed the line, color is BLACK
        if obj.get_has_crossed():
                color = [0,0,0]
        # Assign each tracked object a color based on its idx (index number)
        else:
            i = obj.get_idx() % len(COLORS)
            color = COLORS[i]

            
        box = [int(round(j)) for j in obj.get_box()]
        cv2.rectangle(im,box[:2],box[2:],color,3)

def display_text_box(img, text):
    """
    Displays a text box on screen
    """
    # Define some parameters for the text box
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 3
    thickness = 2
    color = (255, 255, 255) # white color
    background_color = (0, 0, 0) # black color
    padding = 10 # padding around the text
    
    # Get the size of the text box and calculate the position
    text_size, _ = cv2.getTextSize(text, font, font_scale, thickness)
    x = padding
    y = img.shape[0] - padding - text_size[1]
    
    # Draw the text box and the text on top of the image
    cv2.rectangle(img, (x, y), (x + text_size[0] + padding, y + text_size[1] + padding), background_color, -1)
    cv2.putText(img, text, (x + padding // 2, y + text_size[1] + padding // 2), font, font_scale, color, thickness)

def get_boxes(result):
    instances = result.pred_instances.numpy().cpu()
    boxes = instances['bboxes']
    return boxes
def single_image_inference():
    # Build the model from a config file and a checkpoint file
    model = init_detector(args.config, args.checkpoint.format(args.epoch), device='cuda:0')

    # Init visualizer
    visualizer = VISUALIZERS.build(model.cfg.visualizer)
    # The dataset_meta is loaded from the checkpoint and
    # then pass to the model in init_detector
    visualizer.dataset_meta = model.dataset_meta

    # Test a single image and show the results
    img = mmcv.imread(args.sample)  # or img = mmcv.imread(img), which will only load it once
    result = inference_detector(model, img)

    # import IPython; IPython.embed(); import sys; sys.exit()

    # Show the results
    img = mmcv.imread(img)
    img = mmcv.imconvert(img, 'bgr', 'rgb')

    visualizer.add_datasample(
        'result',
        img,
        data_sample=result,
        draw_gt=False,
    
        show=True)
def main():
    # Build the model from a config file and a checkpoint file
    model = init_detector(args.config, args.checkpoint.format(args.epoch), device='cuda:0')

    # Test a video and show the results
    # Build test pipeline
    model.cfg.test_dataloader.dataset.pipeline[0].type = 'LoadImageFromNDArray'
    test_pipeline = Compose(model.cfg.test_dataloader.dataset.pipeline)

    # Reader Video
    # cam = cv2.VideoCapture(args.input)
    cam = StreamReader(args.input)
    cv2.namedWindow(VIDEO, 0)

    i = -1
    t = SubTimer()
    t.tic()
    
    tracker = Tracker(printout=False,object_reset_threshold=60)
    counter = Counter(args.cross)
    #counter = CounterReplay(args.cross)
    aggregator = Aggregator(n_seconds=60)
    #aggregator = AggregatorReplay(n_frames=600)
    while True:
        i+=1
        ret,frame = cam.read()
        if not ret:
            break

        if (i % args.interval)!=0:
            continue
        #Crop frame
        crop = args.crop
        frame = frame[crop[0]:crop[1],crop[2]:crop[3]]

        
        result = inference_detector(model, frame, test_pipeline=test_pipeline)
        t.toc('inference')
        boxes = get_boxes(result)
        boxes = filter_boxes(boxes)

        #Track the object boxes
        tracker.track(boxes)
        t.toc('tracking')

        # Check whether object crosses line
        counter.check_crosses(tracker.get_objects())
        results = counter.get_results()

        
        #Visualize
        visualize_line(frame,args.cross)
        visualize_tracker(frame,tracker)
            

        # Get counts and display that on image
        display_text_box(frame,f"{results}")

        cv2.imshow(VIDEO,frame)
        chd = cv2.waitKey(1)

        # Print results to file and reset counts
        if aggregator.check() or (chd==ord('r')):
            counter.print_results()
            counter.reset()

        
        t.toc('imshow')
        if chd==ord('q'):
            break

    # total = 0
    # print("\nTimes\n=========================")
    # for k,v in t.get_info().items():
    #     print(f"{k} : {v}")
    #     total+= v
    # fps = 200.0 / total
    # print(f"FPS: {fps}")

    cv2.destroyAllWindows()

if __name__=='__main__':
    if args.single:
        single_image_inference()
    else:
        main()
