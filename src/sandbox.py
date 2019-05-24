
import numpy as np
from colorama import Fore, Back, Style, init
import random
import pprint

def testScripts():
    halfOfTheUsers = 9
    maxArraySize = 5

    selectedUsers = [random.random() for i in range(halfOfTheUsers)]
    print(selectedUsers)

    modulus = halfOfTheUsers % maxArraySize
    fixed = halfOfTheUsers // maxArraySize
    print ("Modulus: {0} / fixed: {1}".format(modulus, fixed))

    for x in range(fixed):
        print ("Array {0} x {1}={2}".format(x, maxArraySize, x*maxArraySize))
        newArray = selectedUsers[(x*maxArraySize):(x*maxArraySize+maxArraySize)]
        print(newArray)
        print("-"*20)
    
    lastArray = selectedUsers[(halfOfTheUsers-modulus):(halfOfTheUsers+modulus)]
    print("LastArray: ")
    print(lastArray)

    userIds = ",".join(map(str, lastArray))
    print (userIds)

def main():    
    testScripts()

if __name__ == "__main__":
    init(autoreset=True)
    main()
