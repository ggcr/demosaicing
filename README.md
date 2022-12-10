# Demosaicing
Digital cameras use **pixel sensors** that capture the amount of light is being percieved in a certain pixel. More precisely, when the camera's shutter button is pressed, light particles or *photons* enter the photosite cavities, our pixel cells.

This **photosite cavities** or pixel cells are monochromatic, or in other words, they are not able to detect colors by itself. The resulting RAW image will be a 2-dimensional array of the light values for each photosite cavities. In order to detect color a **demosaicing** process is done, this process consists in placing a color filter upon the monochromatic RAW image to generate the corresponding 3 channels of Red, Blue and Green and interpolate the resting colours.

## Color filters

Each digital camera brands has its own color filters but the most common known is the **Bayern Filter** or palette. This filter is placed at the top of our photosites cavities and they will only let in the corresponding color.

| Name | Pattern Size | Image |
|-----|-----|-----|
| Bayern Filter | `2x2` | <img width=100 src="https://user-images.githubusercontent.com/57730982/205482603-bec095d1-8325-4d75-9e25-347f35940523.png"/> |

As we can see, we will capture twice as green. This is because the way the human see colors, we are much more sensitive to green than to red or blue. And thus, we are capturing the best representation of an image so that we can see it sharpen and detailed later on.

<p align="center">
    <img width=400 src="https://user-images.githubusercontent.com/57730982/205903954-9288f297-1b51-41f8-9994-b98e47bcba69.png" />
</p>


## Demosaicing

For the process of interpolating the missing channels a bilinear process has been implemented with convolutions operations. Another advanced interpolation method has been implemented, Gradient Correction Interpolation.

![unknown](https://user-images.githubusercontent.com/57730982/206854868-f6530127-d4a6-4071-bfed-89f0e91b70e0.png)

## References

R. Kimmel, “Demosaicing: image reconstruction from color CCD samples,” IEEE Trans. on Image Processing, vol. 8, Sept. 1999.

H. S. Malvar, L. He, R. Cutler, "High Quality linear interpolation for Demosaicing of Bayer-patterned color images". 11, Dec. 2015
