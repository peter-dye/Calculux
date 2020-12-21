# How to make a .icns file for the app icon

### Step 1:
Create 1024 by 1024 pixel image with transparent background.

### Step 2:
Export 10 .png files with the following names and sizes to a folder:

|Filename             |Image Size (in pixels)   |
|---------------------|-------------------------|
|`icon_512x512@2x.png`|1024x1024                |
|`icon_512x512.png`   |512x512                  |
|`icon_256x256@2x.png`|512x512                  |
|`icon_256x256.png`	  |256x256                  |
|`icon_128x128@2x.png`|256x256                  |
|`icon_128x128.png`	  |128x128                  |
|`icon_32x32@2x.png`  |64x64                    |
|`icon_32x32.png`	    |32x32                    |
|`icon_16x16@2x.png`	|32x32                    |
|`icon_16x16.png`	    |16x16                    |

### Step 3:
Add .iconset to the folder and click yes when it asks if you're sure.

### Step 4:
Use the iconutil command (installed by default in MacOS) to make a .icns file:
`iconutil -c icns path/to/iconset`

### Step 5:
Use [](https://www.coolutils.com/online/ICNS-to-ICO) to convert the .icns file
to a .ico file for Windows.

### Source:
Checkout [](https://eshop.macsales.com/blog/28492-create-your-own-custom-icons-in-10-7-5-or-later/) for the full steps. This is where I got all the info presented here.
