inputfilename='sound.wav'
path="D:\\MMH\\project\\sound\\sound.wav" #Path to the audio file
big_num=2000;     #Number of keys generated, The bigger the number the bigger the chaos but at the same time the longer the key generation
# To chain the final binary keys
import itertools;
#To read and write to audio(.wav) files:
from wave import open as wave_open;

def printlst (lst) :
  print('[',lst[0],lst[1],lst[2],lst[3],lst[4],lst[5],'......',len(lst),"items ]")

#key gen
def keygen(x,r,size):
  key=[]
  for i in range(size):
    x=r*x*(1-x)
    key.append(((x*pow(10,16))%256.126))
  return key
print("Key generation:")
a = 0.0123;
b = 3.9159;
printlst(keygen(a,b,big_num)) 

#<----RUN ONLY ONCE PER SESSION! DO NOT KEEP RE-RUNNING
print("Generate Deck keys using chaotic map")
deckey=[]
for i in range(big_num):
  deckey.append(keygen(a,b,big_num)[i] -int(keygen(a,b,big_num)[i]))
#print(deckey)
print(i+1, "keys generated")
print("Deck keys generated using chaotic map")
printlst(deckey)

print("Generate final keys from deck key")
finkey=[]
for i in range(big_num):
  finkey.append(int(str(deckey[i])[-3:])) #lấy 3 kí tự cuối cùng của deckey
print("Final key generted:")
printlst(finkey)

print("Generate binary keys from final keys")
binkey=[]
for i in range(big_num):
  binkey.append(bin(finkey[i]))
print("Binary key generated:")
printlst(binkey)

print("Splitting binary keys on the \'b\' ")
binkey_fin=[]
import re
for i in range(big_num):
  binkey_fin.append(re.findall(r'\d+', binkey[i]))
print("Now we have a list of lists:")
printlst(binkey_fin)

#import itertools
print("Converting list of lists into one list")
merged = list(itertools.chain(*binkey_fin))
print('The merged list is:')
printlst(merged)
print("Deleting the alternate zero values")
del merged[0::2]
print("After removing non zero values we have")
printlst(merged)
print("Converting string to integer:")
mergedfinal = list(map(int, merged))
printlst(mergedfinal)



print("Extract from input audio file")
print(path)
#import wave

w= wave_open("D:\\MMH\\project\\sound\\good-morning.wav",'rb')


channels=w.getnchannels()
print("Number of channels",channels)


framerate=w.getframerate()
print("FrameRate:",framerate)


sampwidth=w.getsampwidth()
print("Sample Width:",sampwidth)


framerate=w.getframerate()
print("FrameRate:",framerate)




print("\nNumber of Frames: ", w.getnframes())
frameslst=[]
for i in range(w.getnframes()):
  frame=w.readframes(1)
  frameslst.append(frame)
  #print(frame)

print("The frames are")
printlst(frameslst)

print("\nNow converting them into integers\n")
intframe=[]
for frame in frameslst :
  int_val = int.from_bytes(frame, "big")
  intframe.append(int_val)
  #print(int_val)

print("The integer frames are:\n")
printlst(intframe)

keysize = len(mergedfinal)
print("The number of key values we have generated :",keysize)

print("The number of byte frames we have :",len(intframe))


print("XOR - ENCRYPTION") 

xor_result=[]

for i in range(len(intframe)):
  xor=intframe[i]^mergedfinal[i%keysize] # m mod n returns a value only from 0 to n , no matter how large m is 
  xor_result.append(xor)

print("The XOR result is:")
printlst(xor_result)

#Convert XOR Result to bytearray

check=[]
print("Now converting XOR values into frames:")
for num in xor_result:
  bytes_val = num.to_bytes(4, 'big')
  #print(bytes_val)
  check.append(bytes_val)
check.reverse()
print("\nBytes list\n")
printlst(check)

#code to convert bytearray to wav audio file

print("Now writing the encypted values to an audio file")
filename='encrypted-'+inputfilename

 
writer=wave_open("D:\\MMH\\project\\sound\\"+filename,'wb')

writer.setnchannels(channels)
writer.setsampwidth(sampwidth)
writer.setframerate(framerate)
writer.setnframes(1)
for frame in check:
 writer.writeframesraw(frame)
writer.close()

print("Written to file ", filename)

