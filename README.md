# About
Steganography is the technique of hiding data in appropriate multimedia carrier, e.g, image, audio or video files. The most common method is by embedding information into digital images. In this metod we hide message into new picture, these changes are unnoticable for the human eye. In this project we are using LSB method for hidding message.
## Last Signigicant Bit
In LSB technique is message hidded inside an image by replacing each pixel's least significant bit with bits of the message to be hidden.
Digital image is represented by pixels. Each pixel contains values depending on its type and depth. The most widely used modes are RGB and RGBA.
RGB modes is represented by 3x8-bit pixels, and for RGBA its 4x8 bit pixels. Each bit has values range from 0-255.
# Installation
1. Download this repository
2. Install libraries by writing this to CMD

   `pip install numpy`
   
   `pip install pillow`
   
   `pip install hashlib`
# Usage
## Encryption
To hidding data into the picture we use **App.py**. For the program to function you need to add these arguments:

`python3 App.py -h ./data/[Name of the file].[File format] "[Message]"`
- **Name of the file** - Write exact name of the file. File has to be saved in data folder
- **File format** - Write file format. Our program works with two file formats. **.png** and **.jpg**
- **Message** - Message you want to encrypr to picture

New picture is saved into data folder
## Decryption
To expose hidden data from the picture we use **App.py**. For the program to function you need to add these arguments:

`python3 App.py -g ./data/[Name of the file].[File format]`
- **Name of the file** - Write exact name of the file. File has to be saved in data folder
- **File format** - Write file format. Our program works with two file formats. **.png** and **.jpg**

Hidden data are visible in terminal
## Example
This is example for specific image. After downloading repository and installing needed libraries, open terminal in your project. In data folder, there are three images, so choose on of them or, put there your own picture. For this example, we chose image lol.png. To encrypt this picture write this specific command to your terminal.

`python3 App.py -h ./data/lol.png`

Then you are asked to write in message, so write there for example Hi and press enter. Now, there will appear new picture with data folder with name lol_stego.png and that's your picture with hidden data

Next example is for decryption. Once you did the encryption, you can try do decrypt your image. You should have image with name_stego.[format] in your data folder, if not, just make enryption process for image you want or put your own image with _stego to data folder. I chose this image lol_stego.png, so write this command to your terminal.

`python3 App.py -h ./data/lol_stego.png`

Now you can see hidden message and hashes in terminal. If the hashes are the same, everything is alright and noone tried change your data. Hash is security feature, which tells you if someone tried to manage your image or not.

# Telegram
# Image comparison
Original picture          |  Picture with message
:-------------------------:|:-------------------------:
![](data/lol.png)  |  ![](data/lol_stego.png)
# Authors
- Roman Klampar - files, PNG format
- Michal Kaiser - decode function, presentation
- Ondrej Chudacek - files, JPG format
- Petr Kriz - encode function, read.me
