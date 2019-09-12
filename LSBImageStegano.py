# Python program implementing Image Steganography along with AES Cryptography

# PIL module is used to extract pixels of image and modify it
from PIL import Image
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
import random

key = b'my secret key123'
iv = b'this is sampleiv'


def encrypt(key, iv, data ="Default data"):

    while len(data) % 16 != 0:
        data += 'z'

    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(data.encode(encoding='windows-1252').strip())
    return ciphertext


def decrypt(key, iv, ciphertext):
    ciphertext = ciphertext.encode(encoding='windows-1252')
    cipher = AES.new(key, AES.MODE_CBC, iv)
    data = cipher.decrypt(ciphertext)

    decoded_data = data.decode(encoding='windows-1252')
    #print('decoded: ', decoded_data)

    return decoded_data


def genData(data):   # Converts data into 8-bit binary form
    
    # list of binary codes of given data
    newd = []

    for i in data:
        newd.append(format(ord(i), '08b'))  #ord for ascii 08b for binary

    print('type of newd: ', type(newd))
    return newd


def modPix(pix, data):
    datalist = genData(data)
    lendata = len(datalist)
    imdata = iter(pix)

    for i in range(lendata):

        # Extracting 3 pixels at a time (since 3 pixels = 3 * 3(rgb) = 9 values)
        # 8 values for representing data, last value to signal if the data continues
        pix = [value for value in imdata.__next__()[:3] +
               imdata.__next__()[:3] +
               imdata.__next__()[:3]]

        # odd for 1 and even for 0
        for j in range(0, 8):
            if (datalist[i][j] == '0') and (pix[j] % 2 != 0):

                if (pix[j] % 2 != 0):
                    pix[j] -= 1

            elif (datalist[i][j] == '1') and (pix[j] % 2 == 0):
                pix[j] -= 1

        # 0 means keep reading; 1 means the message is over.
        if (i == lendata - 1):
            if (pix[-1] % 2 == 0):
                pix[-1] -= 1
        else:
            if (pix[-1] % 2 != 0):
                pix[-1] -= 1

        pix = tuple(pix)
        yield pix[0:3]  #The yield statement suspends function’s execution and sends a value back to caller,
        yield pix[3:6]  # but retains enough state to enable function to resume where it is left off.
        yield pix[6:9]


def encode_enc(newimg, data):
    w = newimg.size[0]
    (x, y) = (0, 0)

    for pixel in modPix(newimg.getdata(), data):

        # Putting modified pixels in the new image
        newimg.putpixel((x, y), pixel)
        if (x == w - 1):
            x = 0
            y += 1
        else:
            x += 1


def encode():
    img = input("Enter image name(with extension): ")
    image = Image.open(img, 'r')

    data = input("Enter data to be encoded : ")
    if (len(data) == 0):
        raise ValueError('Data is empty')

    newimg = image.copy()
    encrypted_data = encrypt(key, iv, data)
    print('encrypted data: ', encrypted_data)

    encrypted_data = encrypted_data.decode(encoding='windows-1252')
    print('encrypted decoded: ', encrypted_data, ' encoded agn: ', encrypted_data.encode(encoding='windows-1252'))

    #print('decrypted here: ', decrypt(key, iv, encrypted_data))

    encode_enc(newimg, encrypted_data)

    new_img_name = input("Enter the name of new image(with extension): ")
    newimg.save(new_img_name, str(new_img_name.split(".")[1].upper()))


def decode():
    img = input("Enter image name(with extension) :")
    image = Image.open(img, 'r')

    data = ''
    imgdata = iter(image.getdata())

    while (True):
        pixels = [value for value in imgdata.__next__()[:3] +
                  imgdata.__next__()[:3] +
                  imgdata.__next__()[:3]]
        # string of binary data
        binstr = ''

        for i in pixels[:8]:
            if (i % 2 == 0):
                binstr += '0'
            else:
                binstr += '1'

        data += chr(int(binstr, 2))
        if (pixels[-1] % 2 != 0):
            print('data before decrypting: ', data)
            data = decrypt(key, iv, data)
            return data


def main():
    a = int(input("LSB Image Steganography ::\n"
                  "1. Encode\n2. Decode\n"))
    if (a == 1):
        encode()

    elif (a == 2):
        print("Decoded word- " + decode())
    else:
        raise Exception("Enter correct input")


if __name__ == '__main__':
    main()

