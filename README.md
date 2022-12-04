# Demosaicing
Digital cameras use **pixel sensors** that capture the amount of light is being percieved in a certain pixel. More precisely, when the camera's shutter button is pressed, light particles or *photons* enter the photosite cavities, our pixel cells.

This **photosite cavities** or pixel cells are monochromatic, or in other words, they are not able to detect colors by itself. The resulting RAW image will be a 2-dimensional array of the light values for each photosite cavities. In order to detect color a **demosaicing** process is done, this process consists in placeing a color filter upon the monochromatic RAW image to generate the corresponding 3 channels of Red, Blue and Green.

## Normalization

First of all, RAW images are captured in a `uint16` type, that is, in values of range from 0 to 65536 (2^16). And for convention we work with RGB images of `uint8` in ranges of 0 up until 255. So we first need a process to **normalize** our image.

This is nicely done with the following formula:



Corresponding in the following code:

```python
def normalize(img, maxval, minval):
    """
    https://en.wikipedia.org/wiki/Normalization_(image_processing)
    """
    return (np.rint((img - img.min()) * ((maxval - minval) / (img.max() - img.min())) + minval)).astype(dtype='uint8')
```

## Color filters

Each digital camera brands has its own color filters but the most common known is the **Bayern Filter** or palette. This filter is placed at the top of our photosites cavities and they will only let in the corresponding color.

| Name | Pattern Size | Image |
|-----|-----|-----|
| Bayern Filter | `2x2` | <img width=100 src="https://user-images.githubusercontent.com/57730982/205482603-bec095d1-8325-4d75-9e25-347f35940523.png"/> |

As we can see, we will capture twice as green. This is because the way the human see colors, we are much more sensitive to green than to red or blue. And thus, we are capturing the best representation of an image so that we can see it sharpen and detailed later on.


