### STEP 6 : Decryption and retrieval of audio file
#Path to the audio file
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
a = 0.0125;
b = 3.9159;
printlst(keygen(a,b,big_num)) 

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

xor_result=[]

with open("D:\\MMH\\MMHproject\\MMH\\output.txt", "r") as f:
  for line in f:
    xor_result.append(int(line.strip()))

orig=[]
#print("The integer frames are:")
#print(intframe)

for i in range(len(xor_result)):
  xor=xor_result[i]^mergedfinal[i%len(mergedfinal)]
  orig.append(xor)

print("The decrypted result is:")
#xor_result.reverse()
printlst(orig)


checked=[]
print("Now converting them back into frames:")
for num in orig:
  bytes_val = num.to_bytes(4, 'big')
  #print(bytes_val)
  checked.append(bytes_val)
#print("\nBytes list\n")
printlst(checked)

#Write to an audio file
print("Now we write the values back into a audio file")

filename='decryptedsound.mp3'
 
writer=wave_open("D:\\MMH\\MMHproject\\MMH\\sound\\"+filename,'wb')
framelst1 = []
with open("D:\\MMH\\MMHproject\\MMH\\output1.txt", "r") as f:
  for line in f:
    framelst1.append(int(line.strip()))

  
writer.setnchannels(framelst1[0])
writer.setsampwidth(framelst1[1])
writer.setframerate(framelst1[2])
writer.setnframes(1)
for frame in checked:
 writer.writeframesraw(frame)
writer.close()

print("Written to file ", filename)