#!/Users/gustavoaguilar/anaconda3/envs/py35/bin/python
"""dip_hw1.py: Starter file to run howework 1"""

#Example Usage: ./dip_hw1_region_analysis -i imagename.jpg


__author__      = "Pranav Mantini"
__email__ = "pmantini@uh.edu"
__version__ = "1.0.0"

import cv2
import sys
from datetime import datetime
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from region_analysis import binary_image as bi
from region_analysis import cell_counting as cc

def display_image(window_name, image):
    """A function to display image"""
    cv2.namedWindow(window_name)
    cv2.imshow(window_name, image)
    cv2.waitKey(0)


def main():
    """ The main funtion that parses input arguments, calls the approrpiate
     interpolation method and writes the output image"""

    #Parse input arguments
    from argparse import ArgumentParser

    parser = ArgumentParser()

    parser.add_argument("-i", "--image", dest="image",
                        help="specify the name of the image", metavar="IMAGE")

    args = parser.parse_args()

    #Load image
    if args.image is None:
        print("Please specify the name of image")
        print("use the -h option to see usage information")
        sys.exit(2)
    else:
        image_name = args.image.split(".")[0]
        input_image = cv2.imread(args.image, 0)

    hist = bi.compute_histogram(input_image)

    outputDir = 'output/cellct/'

    # Saving histogram to output directory
    hist_fig = plt.plot(hist)
    plt.savefig(outputDir+image_name+"-hist.png")

    threshold = bi.find_optimal_threshold(hist)
    print("Optimal threshold: ", threshold)

    binary_img = bi.binarize(input_image, threshold)
    output_image_name = outputDir + "binary_image_" + datetime.now().strftime("%m%d-%H%M%S") + ".jpg"
    cv2.imwrite(output_image_name, binary_img)

    # blobcoloring
    regions = cc.blob_coloring(binary_img)
    stats = cc.compute_statistics(regions)

    cell_stats_img = cc.mark_regions_image(regions, stats)
    output_image_name = outputDir + "cell_stats_" + datetime.now().strftime("%m%d-%H%M%S") + ".jpg"
    cv2.imwrite(output_image_name, cell_stats_img)

if __name__ == "__main__":
    main()







