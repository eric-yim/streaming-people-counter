import matplotlib.pyplot as plt
import numpy as np
import os, glob
import matplotlib.patches as patches
import random
DIRECTORY = 'boxes'
IMG_DIMS = [1080,1920,3]
WINDOW0 = 'image'
def max_line(y):
    return 800 + (y*8.5)
def min_line(y):
    return -1800 + (y*6)
def get_npy_names():
    return sorted(glob.glob(os.path.join(DIRECTORY,'*.npy')))
def load_npy_files(names):
    return [np.load(name) for name in names]
def flatten(npy_arrs):
    return np.concatenate(npy_arrs,axis=0)

def plot_axes(x,y,image,rect_coords):
    fig, (ax1, ax2) = plt.subplots(2,1, figsize=(10, 5))

    # Plot the scatter plot on the left axis
    ax1.scatter(x, y)
    boundary_y = np.linspace(150,1080,3)
    max_area = max_line(boundary_y)
    ax1.plot(max_area,boundary_y,'r')
    boundary_y = np.linspace(600,1080,3)
    min_area = min_line(boundary_y)
    ax1.plot(min_area,boundary_y,'r')
    ax1.set_xlabel('Box Width (pixels)')
    ax1.set_ylabel('Y of Center (pixels)')
    ax1.invert_yaxis() 
    ax1.set_title('Scatter Plot')

    # Display the image on the right axis
    ax2.imshow(image, cmap='gray')
    ax2.set_title('Image')
    for rect in rect_coords:
        rect_patch = patches.Rectangle((rect[0], rect[1]), rect[2], rect[3], linewidth=2, edgecolor='g', facecolor='none')
        ax2.add_patch(rect_patch)
    plt.show()
def convert_rect_coords(rect):
    x0, y0, x1, y1 = rect
    w = x1 - x0
    h = y1 - y0
    return [x0,y0,w,h]
def calculate_stats(all_boxes):
    # X is height of box
    heights = all_boxes[:,3] - all_boxes[:,1]
    widths = all_boxes[:,2] - all_boxes[:,0]

    y = ((all_boxes[:,3]+all_boxes[:,1])/2)

    # Y is height/width ratio
    # ratios = heights/widths
    area = heights * widths
    return area, y
def main():
    # cv2.namedWindow(WINDOW0, 0)
    npy_names = get_npy_names()
    random.shuffle(npy_names)
    for npy_name in npy_names:
        npy_arr = np.load(npy_name)
        img = np.zeros(IMG_DIMS,dtype=np.uint8)
        widths, y = calculate_stats(npy_arr)
        rects = [convert_rect_coords(rect) for rect in npy_arr]
        plot_axes(widths,y,img,rects)

    
    
    
    
if __name__=='__main__':
    main()