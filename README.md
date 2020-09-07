# Greyscale Image Reconstruction Based On Singular Value Decomposition

Reconstruct a `.png` image with Singular Value Decomposition.  Shows matrix reconstruction sums for diagnoal matrix values `n=1,2,3,4,5,10,25,50,100` beside the orignal matrix. Also shows plots of the magnitude of the diagnoal values as well as their cumulative sum.

## Screenshot

![Failed to load screenshot](/svd_doge_screenshot.png?raw=true "Greyscale Image Reconstruction With SVD Screenshot")

## Requirements 

Requires `numpy`, `opencv-python`, `matplotlib` and `pysimplegui`.

Install via `pip` with:

```shell
python3 -m pip install numpy
python3 -m pip install opencv-python
python3 -m pip install matplotlib
python3 -m pip isntall pysimplegui
```

## Usage

Using browse, select a local `.png` image.  Pressing the `Reconstruct my image!` button will popular the `3x3` reconstruction image grid and show to graph that analyze the effectiveness of the `Sigular Value Decomposition` on the particular image.  Also shows the original image. 

> **__NOTE:__** All images are converted to `greyscale` then scaled down to `150x150` which may cause some distortion in the original image and therefore the reconstructions.  As a result, discripencies may occur between the true original and the scaled original - take the later to be the goal of the program.
