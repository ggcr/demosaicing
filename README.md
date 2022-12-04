# Demosaicing
Digital cameras use **pixel sensors** that capture the amount of light is being percieved in a certain pixel. More precisely, when the camera's shutter button is pressed, light particles or *photons* enter the photosite cavities, our pixel cells.

This **photosite cavities** or pixel cells are monochromatic, or in other words, they are not able to detect colors by itself. The resulting RAW image will be a 2-dimensional array of the light values for each photosite cavities. In order to detect color a **demosaicing** process is done, this process consists in placeing a color filter upon the monochromatic RAW image to generate the corresponding 3 channels of Red, Blue and Green.

## Color filters
Each digital camera brands has its own color filters but the most common known are:

| Name | Pattern Size | Image |
|-----|-----|-----|
| Bayern Filter | `2x2` | <img width=100 src="https://user-images.githubusercontent.com/57730982/205482603-bec095d1-8325-4d75-9e25-347f35940523.png"/> |

