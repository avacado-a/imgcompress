#IMPORTS#
import Image
import random
import math
import sys
import time
import numpy
#FUNCTIONS#
def to_binary(value, length):
    binary_str = ""
    for _ in range(length):
        binary_str = str(value & 1) + binary_str
        value >>= 1
    return binary_str
def power(x, y, m):
    if (y == 0):
        return 1
    p = power(x, y // 2, m) % m
    p = (p * p) % m
 
    return p if(y % 2 == 0) else (x * p) % m
def primality(p):
  for i in range(2):
    a= random.randint(1,p-1)
    if power(a,p-1,p)== 1:
      pass
    else:
      return False
      break
  return True
def return2factors(n):
  lists = []
  for i in  range(1,int(n**0.5)):
    if n%i==0:
      lists.append(i)
  if n==1 or primality(n):
    print(f"Switching {n} to {n+1}")
    return return2factors(n+1)
  xes = (lists[int(len(lists))-1],int(n/lists[int(len(lists))-1]))
  print(len(lists),lists,n,xes)
  return xes
    
def setx(x:str,r,g,b,a):
  if False in [i in ["0","1"] for i in x]:
    raise TypeError("Argument x contained a non binary character.")
  if len([i for i in x]) !=3:
    raise ValueError("String contains more that 3 binary digits.")
  if r%2 != int(x[0]):
    if r!=255:
      r+=1
    else:
      r-=1
  if g%2 != int(x[1]):
    if g!=255:
      g+=1
    else:
      g-=1
  if b%2 != int(x[2]):
    if b!=255:
      b+=1
    else:
      b-=1
  return (r,g,b,a)

def setxtra(x:str,r,g,b,a,dataloss = 5):
  lesser = 8-dataloss
  cutval = 2**lesser
  if False in [i in ["0","1"] for i in x]:
    raise TypeError("Argument x contained a non binary character.")
  if len([i for i in x]) !=lesser*3:
    raise ValueError("String contains more that 3 binary digits.")
  if r%cutval != int(x[:lesser],2):
    r = (r//cutval)*cutval
    r+=int(x[:lesser],2)
  if g%cutval != int(x[lesser:2*lesser],2):
    g = (g//cutval)*cutval
    g+=int(x[lesser:2*lesser],2)
  if b%cutval != int(x[2*lesser:],2):
    b = (b//cutval)*cutval
    b+=int(x[2*lesser:],2)
  return (r,g,b,a)

def getxtra(r,g,b,a,dataloss=5):
  lesser = 8-dataloss
  cutval = 2**lesser
  return "".join([str(bin((i%cutval)+cutval)[3:]) for i in [r,g,b]])
def getbinary(r,g,b,a):
  return "".join([str(i%2) for i in (r,g,b)])
def prints(boolean, *args,end="\n"):
  if boolean:
    print(args,end="\n")

def encodeBinString(message,filename,tofilename="new.png",dataloss=5,overridesize=False,desc = False):
  try:
    image = Image.open(filename)#Lowering the image resolution as it will take a long time to run on a high resolution
  except:
    return IndexError("File does not exist.")
  if not overridesize:
    image.thumbnail((600,600))
  image.save(tofilename)
  img = Image.open(tofilename)# Opening the smaller image 
  img_size=img.size #Getting the image size
  arr = list(img.getdata()) #Loading the Image data into RAM
  prints(desc,"Image data in RAM")
  message+="1"# End of message indicator
  while len(message)%(3*(8-dataloss))!=0:
    message+="0" # So the message is completely balanced when read (If I am alive, I will explain...)
  prints(desc,"Image ready to send")
  mesidx = 0 # Keeps track of what index of message to encode.
  count= 0 # Keeps track of used and extra space left in the image.
  for i in range(len(arr)):
    prints(desc,str(round((100*i)/len(arr),2))+"%",end = "\r")
    try:#Get the r,g,b,a values of a color
      r,g,b,a = arr[i]
    except:
      r,g,b = arr[i]
      a = 255
    try: # If there is more message to send, send it, or else just send 0's
      answer = setxtra(message[mesidx:mesidx+3*(8-dataloss)],r,g,b,a,dataloss = dataloss)
    except BaseException as e:
      count+=1 #Counts the extra data
      answer = setxtra("".join(["0" for i in range(3*(8-dataloss))]),r,g,b,a,dataloss=dataloss)
    arr[i] = answer
    mesidx+=3*(8-dataloss)
  if count == 0:
    raise BaseException("Not enough space to store image")
  prints(desc,"Extra bits left",count*3*(8-dataloss),len(message))
  im2 = Image.new(mode="RGBA", size=img_size)# Store the image data into a real image
  im2.putdata(arr)
  im2.save(tofilename)

def decodeBinString(filename,overidesize=False,dataloss=5,desc=False):
  try: # Try opening the file
    img = Image.open(filename)
  except:
    return IndexError("File does not exist")
  arr = list(img.getdata()) # Get the image data into RAM
  prints(desc,"Image data in RAM")
  message = "" #The emtpy binary string
  prints(desc,"Starting Decode")
  for i in range(len(arr)):
    prints(desc,i*100/len(arr),"percent done decode",end="\r")
    try: # Get the RGBA value
      r,g,b,a = arr[i]
    except:
      r,g,b = arr[i]
      a = 255

    message += getxtra(r,g,b,a,dataloss=dataloss) # Add the binary value to the list of all binary values.
  prints(desc,"Processed image!")
  while not "1" in message[-100:]:# Get rid of the extra zeros at the end.
    message = message[:len(message)-100]
  while message[-1] == "0":
    message = message[:len(message)-1]
  message = message[:len(message)-1]# Getting rid of the extra 1 added to make the message completely whole.
  return message
def mismatch_index(str1, str2):
  #Finds the index at which two strings stop matching.
  for i in range(min(len(str1), len(str2))):
    if str1[i] != str2[i]:
      return i
  return min(len(str1), len(str2))

def compress(percent:float,filename,tofilename = "gmonkey.png",saved_image_readability = True):
  a = [0.875,0.75,0.624,0.5,0.377,0.25,0.126]
  #dataloss = originalloss #This is the amount of bits(out of 8) will be kept. The lower this number, the lower the quality, but the smaller the saved image can be.
  saved_image_readability = True # The cropped image will have some resemblance to the original when set True
  imagecrop = percent
  #filename = "thisisis.png"
  #tofilename = "gmonkey.png"

  img = Image.open(filename)
  img_size=img.size
  arr = list(img.getdata())
  s = 0
  while a[s]>percent:
    s+=1
    if s==len(a):
      raise BaseException("We cannot compress the image that much!")
  dataloss = 7-s
  if img_size[1]<25:
    raise BaseException("Image too small :(")
  big = []
  small = []#list(img_size)
  big_limit = round(img_size[1]*imagecrop)*img_size[0] if saved_image_readability else round(imagecrop*len(arr))

  for i in range(len(arr)):
    if i<big_limit:
      big.append(arr[i])
    else:
      for x in range(len(arr[i])):
        if x < 3:
          small.append(arr[i][x])

  a = [bin(i)[2:].zfill(dataloss) for i in range(2**dataloss)] 

  smallstr = ""

  ahs = bin(img_size[0])[2:]
  while len(ahs)!=13:
    ahs="0"+ahs
  smallstr+=ahs
  ahs = bin(img_size[1])[2:]
  while len(ahs)!=13:
    ahs="0"+ahs
  smallstr+=ahs

  small_values = [math.floor(small[i] / (2**(8-dataloss))) for i in range(len(small))]

  smallstr += "".join([a[small_values[i]] for i in range(0,len(small_values))])

  im2 = Image.new(mode="RGB", size=(img_size[0],round(img_size[1]*imagecrop)))
  im2.putdata(big)
  im2.save(tofilename)

  encodeBinString(smallstr,tofilename,tofilename,dataloss=dataloss)#High Time Consumption

def uncompress(percent,filename,tofilename = "mew3.png"):
  a = [0.875,0.75,0.624,0.5,0.377,0.25,0.126]
  s = 0
  while a[s]>percent:
    s+=1
    if s==len(a):
      raise BaseException("We cannot compress the image that much!")
  dataloss = 7-s
  size = []
  smaller = []
  x = 0

  answers = decodeBinString(filename,dataloss = dataloss)

  for y in range(2):
    abs = ""
    for i in range(13):
      abs+=answers[x]
      x+=1
    size.append(int(abs, 2))
  while x < len(answers):
    abs = ""
    for i in range(dataloss):
      abs+=answers[x]
      x+=1
    smaller.append(int(abs, 2)*(2**(8-dataloss)))

  img = Image.open(filename)
  img_size=img.size
  newbig = list(img.getdata())

  for i in range(len(newbig)):
    if len(newbig[i])==4:
      newbig[i]=newbig[i][:3]

  length = len(smaller)
  newbig += [(smaller[x], smaller[x+1], smaller[x+2]) for x in range(0, length-2, 3)]

  im2 = Image.new(mode="RGB", size=tuple(size))
  im2.putdata(newbig)
  im2.save(tofilename)
#SETUP#
sys.set_int_max_str_digits(10**9)
#CODING#

compress(0.76,"original.png","compressed.png")
uncompress(0.76,"compressed.png","uncompressed.png")
  

#--------------------------------------------------------------#
