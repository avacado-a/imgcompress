# imgcompress
## Before using any code, please read the LICENSE file.
All of the code needed is in the encompress.py file.
The only function you need are compress and uncompress
```python
filename = "Filename of file you want to compress here"
tofilename = "Filename the compressed image goes to"
compressfactor = 0.9#Put a number between 0 and 1 that represent how compressed you want the image. The more compressed, the lower quality uncompressed image will be.
compress(compressfactor,filename,tofilename)
```
```python
filename = "Filename of file you want to uncompress here"
tofilename = "Filename the uncompressed image goes to"
compressfactor = 0.9 #Put how compressed the image is (between 0 and 1) This is the same number you put when making the image
uncompress(compressfactor,filename,tofilename)
```
