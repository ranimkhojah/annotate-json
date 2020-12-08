import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.patches as patches
import json
import sys

def annotate(file):

    fig, ax = plt.subplots(figsize=[9,4])
    img = mpimg.imread(str(file)+'.jpg')
    imgplot = plt.imshow(img)

    v1= 0
    v2= 0

    # all annotations for vehicles
    with open (str(file)+'_judgements.json', 'r') as read_file:
        data = json.load(read_file)
        for ann in data:
            for obj in data[ann]:
                if obj['type'] == 'Vehicle':
                    for el in obj['boundaries']:
                        for coords in el['boundaryPoints']:

                            if coords['edge'] == 'Bottom':
                                bottom = coords['coords']
                            if coords['edge'] == 'Top':
                                top = coords['coords']
                            if coords['edge'] == 'Left':
                                left = coords['coords']
                            if coords['edge'] == 'Right':
                                right = coords['coords']


                        width = left[0] - right[0]
                        height = top[1] - bottom[1]
                        rect = patches.Rectangle((bottom[0], bottom[1]), width, height, linewidth=1, edgecolor='purple', facecolor='none')
                        ax.add_patch(rect)

                # save two annotations for object 2
                if v1==0:
                    if obj['properties'] == {"ObjectID": 2}:
                        vehicle_1 = patches.Rectangle((bottom[0], bottom[1]), width, height, linewidth=1, edgecolor='r', facecolor='none')
                        rec_1= [bottom[0],bottom[1],width, height]
                        rec_1_area = (rec_1[1] - rec_1[0]) * (rec_1[3] - rec_1[2])
                        v1= 1

                elif v2==0:
                    if obj['properties'] == {"ObjectID": 2}:
                        vehicle_2 = patches.Rectangle((bottom[0], bottom[1]), width, height, linewidth=1, edgecolor='r', facecolor='none')
                        rec_2= [bottom[0],bottom[1],width, height]
                        rec_2_area = (rec_2[1] - rec_2[0]) * (rec_2[3] - rec_2[2])
                        v2= 1


    plt.draw()
    plt.show()

    #display two annotations in another figure:
    fig, ax = plt.subplots(figsize=[9,4])
    img = mpimg.imread(str(file)+'.jpg')
    imgplot = plt.imshow(img)

    ax.add_patch(vehicle_1)
    ax.add_patch(vehicle_2)

    #intersection coordinates
    inter_left = max(rec_1[0], rec_2[0])
    inter_right = min(rec_1[1], rec_2[1])
    inter_top = max(rec_1[2], rec_2[2])
    inter_bottom = min(rec_1[3], rec_2[3])

    inter_area = (inter_right - inter_left) * (inter_bottom - inter_top)
    unioun_area = (rec_1_area + rec_2_area) - inter_area
    IOU = inter_area / unioun_area

    print('area 1: ', rec_1_area)
    print('area 2: ', rec_2_area)
    print('unioun area: ', unioun_area)
    print('intersection area: ', inter_area)
    print('IOU: ',IOU)

    plt.draw()
    plt.show()

    return 1

def main():
    dir = sys.argv[1]
    annotate(dir)

if __name__ == '__main__':
    main()
