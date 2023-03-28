import numpy as np
from PIL import Image
import os
import matplotlib.pyplot as plt
HIT = 1
STAY = 0

def vizMConline(url): #! for MC online

    input_array = np.load(url)

    # Define the colors for the table cells
    blue = (0, 0, 255) 
    red = (255, 0, 0)#! hit

    # Create the output image as a 2D array of pixels
    image_array = np.zeros((input_array.shape[0], input_array.shape[1], 3), dtype=np.uint8)

    # Set the colors of the pixels based on the input array
    for i in range(input_array.shape[0]):
        for j in range(input_array.shape[1]):
            if input_array[i, j ,0] > input_array[i, j ,1]:
                image_array[i, j] = blue
            else:
                image_array[i, j] = red

    # Create a PIL Image object from the pixel array
    image = Image.fromarray(image_array)
    image = image.resize((image_array.shape[1]*200,image_array.shape[0]*200))

    # Save the image to a file
    file_name = os.path.splitext(os.path.basename(url))[0]
    file_name = os.path.join('data',file_name)
    image.save(file_name+".png")

def vizOptimalTable(url):
    input_array = np.load(url)
    blue = (0, 0, 255) 
    red = (255, 0, 0)#! hit
    image_array = np.zeros((input_array.shape[0], input_array.shape[1], 3), dtype=np.uint8)
    for i in range(input_array.shape[0]):
        for j in range(input_array.shape[1]):
            if input_array[i, j] == STAY :
                image_array[i, j] = blue
            else:
                image_array[i, j] = red

    # Create a PIL Image object from the pixel array
    image = Image.fromarray(image_array)

    # Save the image to a file
    file_name = os.path.splitext(os.path.basename(url))[0]
    file_name = os.path.join('data',file_name)
    image.save(file_name+".png")

def vizMoney(url):
    moneys = np.load(url)
    file_name = os.path.splitext(os.path.basename(url))[0]
    plt.plot(moneys,label = file_name)

    plt.grid()
    plt.savefig(os.path.join('data',file_name)+'RealMoneyRealBet3'+'.png')
    plt.show()

# viz("/home/arash/Workdir/BJ/BlackjackAI/hard18000.npy")
# vizMConline("/home/arash/Workdir/BJ/BlackjackAI/hard18000.npy")
# vizMConline("/home/arash/Workdir/BJ/BlackjackAI/hard20000.npy")
# vizOptimalTable("/home/arash/Workdir/BJ/BlackJackHacked/optimalTableHard.npy")
# vizMoney("/home/arash/Workdir/BJ/BlackJackHacked/logs/importantRes/doublefixedmethod1Mon_Mar_27_23_07_48_2023/MoneyRec.npy")
# vizMoney("/home/arash/Workdir/BJ/BlackJackHacked/logs/OptMoneyTestmethod1Mon_Mar_27_23_21_59_2023/MoneyRec.npy")
# vizMoney("/home/arash/Workdir/BJ/BlackJackHacked/logs/OptMoneyTestRealMoneySmallBetmethod1Mon_Mar_27_23_35_04_2023/MoneyRec.npy")
# vizMoney("/home/arash/Workdir/BJ/BlackJackHacked/logs/realisticMoney2method1Mon_Mar_27_23_53_20_2023/MoneyRec.npy")
# vizMoney("/home/arash/Workdir/BJ/BlackJackHacked/logs/realisticMoney2method1Mon_Mar_27_23_58_27_2023/MoneyRec.npy")
# vizMoney("/home/arash/Workdir/BJ/BlackJackHacked/logs/realisticMoney2NoDoublemethod1Tue_Mar_28_00_01_05_2023/MoneyRec.npy")
vizMoney("/home/arash/Workdir/BJ/BlackJackHacked/logs/realisticMoney2WDouble2method1Tue_Mar_28_00_22_55_2023/MoneyRec.npy")

