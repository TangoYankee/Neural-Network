import numpy
import math
import csv


#A -> control
#B -> case

class PNN:
    def __init__(self):
        #Run the command to import the data
        self.allData = self.importData()
        #Initialize the Five Folds
        self.Fold1 = self.allData[0]
        self.Fold2 = self.allData[1]
        self.Fold3 = self.allData[2]
        self.Fold4 = self.allData[3]
        self.Fold5 = self.allData[4]
        
        #Create an Array of all the data
        self.allDataArray = numpy.array(self.allData)

        #Create an empty list for the sample data and training data
        self.sampleArray = []
        self.trainArray = []

        #Create Values for the priors and losses
        self.lA = 1
        self.lB = 1
        self.hA = (1-(44/float(102)))
        self.hB = 44/float(102)

        #Create an empty list of working sigmas for each 
        self.sigmaList = list()

    def setLoss(self, lA, lB):
        self.lA =lA
        self.lB =lB
    
    def importData(self):
        #Open the files
        self.imFold1 = open("C:/Users/tm/Documents/Spring 2012/302_breast-cancer/C_fold1.csv", "r")
        self.imFold1Reader = csv.reader(self.imFold1)
        self.imFold2 = open("C:/Users/tm/Documents/Spring 2012/302_breast-cancer/C_fold2.csv", "r")
        self.imFold2Reader = csv.reader(self.imFold2)
        self.imFold3 =open("C:/Users/tm/Documents/Spring 2012/302_breast-cancer/C_fold3.csv", "r")
        self.imFold3Reader = csv.reader(self.imFold3)
        self.imFold4 =open("C:/Users/tm/Documents/Spring 2012/302_breast-cancer/C_fold4.csv", "r")
        self.imFold4Reader = csv.reader(self.imFold4)
        self.imFold5 =open("C:/Users/tm/Documents/Spring 2012/302_breast-cancer/C_fold5.csv", "r")
        self.imFold5Reader = csv.reader(self.imFold5)

        
        #Read The files
        self.imFold1Read = list()
        self.imFold2Read = list()
        self.imFold3Read = list()
        self.imFold4Read = list()
        self.imFold5Read = list()
        

        for row in self.imFold1Reader:
            self.imFold1Read.append(row)
        for row in self.imFold2Reader:
            self.imFold2Read.append(row)
        for row in self.imFold3Reader:
            self.imFold3Read.append(row)
        for row in self.imFold4Reader:
            self.imFold4Read.append(row)
        for row in self.imFold5Reader:
            self.imFold5Read.append(row)

        return (self.imFold1Read, self.imFold2Read, self.imFold3Read, self.imFold4Read, self.imFold5Read)

    def orgFold(self, t, s1, s2, s3, s4):
        dataSample = self.allData[s1]+ self.allData[s2] + self.allData[s3]+ self.allData[s4]
        self.sampleArray = numpy.array(dataSample)
        self.trainArray = numpy.array(self.allData[t])

    def train(self, traitA, startA, stopA, sigmaIntervalA):
        self.trait = traitA
        self.start = startA
        self.stop = stopA
        self.sigmaInterval = sigmaIntervalA
        accuracyRecord = open("Accur.csv","w")

        for y in range(self.start, self.stop):
            sigma = y/float(self.sigmaInterval)
            accuracy = self.runEquation(sigma)
            accuracyRecord.write(str(accuracy)+"\n")

    def setSigmaList(self, s1, s2, s3, s4, s5, s6, s7, s8, s9):
        self.sigmaList = (s1,s2, s3, s4, s5, s6, s7, s8, s9)

    def runPNN(self):
        resultRecord = open("resultRecord.csv", "w")
        #Create A file to cycle through all of the accuracies of each training value
        controlRecord = open("controls.csv", "w")
        correctRec = open("corrects.csv", "w")

        correct = 0
        incorrect = 0 
        total = 0
        casePos = 9
                        
        #Create a for loop to cycle through all of the training pairs
        for t in range(len(self.trainArray)):
            #When moving onto to next training pair and reset the counters and summations
            #Create variables that can record each value to be added and the number by which it will be divided
            controlSumSingle = 0
            caseSumSingle = 0 
            numControls = 0
            numCases = 0

            #Go through each sigma for each training pair
            for y in range(casePos):
                sigma = self.sigmaList[y]
                #Cycle through all of the samples for every sigma at each training pair
                #print(len(self.sampleArray))
                for i in range(len(self.sampleArray)):
                    
                    #Calculate the value of the Summation function For the Given training pair
                    difference = (float(self.sampleArray[i,y]) - float(self.trainArray[t,y]))
                    denominator = 2*(math.pow(sigma,2))
                    numerator = -(math.pow(difference,2))
                    avgDistance = math.exp(numerator/denominator)

                    
                    if (int(self.sampleArray[i,casePos])) == 0:
                        #If it is a control, add it to the control summation function
                        controlSumSingle += avgDistance
                        numControls+=1
        
            
                    else:
                        #If it is a case, add it to the case summation function
                        caseSumSingle += avgDistance
                        numCases+=1






            
        

            #Once all of the sigmas for all of the samples have been cycled through
            #Divide by the number of samples
            #print("numCont",numControls)
            #print("numCase",numCases)
            f_A = controlSumSingle/numControls
            f_B = caseSumSingle/numCases
        
            #Multiply By the Losses and Priors
            controlOutput = (f_A)*(self.lA)*(self.hA)
            caseOutput = (f_B)*(self.lB)*(self.hB)

            #print("Cont", controlOutput)
            #print("Case", caseOutput)
            

            #Chck the Accuracy
            if controlOutput > caseOutput:
                result = 0
            else:
                result = 1

            if result == int(self.trainArray[t,casePos]):
                correct +=1

            else:
                incorrect +=1


            total+=1



            controlRecord.write(str(controlOutput-caseOutput)+"\n")
            resultRecord.write(str(result) + "\n")
            correctRec.write(str(self.trainArray[t,casePos]) + "\n")


        #DEBUG: print(correct)
        #DEBUG: print(total)
        print(correct/float(total))
        controlRecord.close
        resultRecord.close
        correctRec.close
        
        

    def runEquation(self, sigma):
        correct = 0
        incorrect = 0
        total = 0
        casePos = 9
        #Debugging: print("A")
        for t in range(len(self.trainArray)):
            controlSumSingle = 0
            caseSumSingle = 0
            numControls = 0
            numCases = 0
            #Debugging: print("B")
            for i in range(len(self.sampleArray)):

                difference = (float(self.sampleArray[i, self.trait]) - float(self.trainArray[t,self.trait]))
                denominator = 2*(math.pow(sigma,2))
                numerator = -(math.pow(difference, 2))
                avgDistance = math.exp(numerator/float(denominator))
                #Debugging: print("C")
                if (int(self.sampleArray[i,casePos]))==0:
                    controlSumSingle += avgDistance
                    numControls+=1
                    #Debugging: print("D")    

                else:
                    caseSumSingle += avgDistance
                    numCases+=1

            f_A = controlSumSingle/float(numControls)
            f_B = caseSumSingle/float(numCases)

            controlOutput = (f_A)*(self.lA)*(self.hA)
            #Debugging:print(controlOutput)
            caseOutput = (f_B)*(self.lB)*(self.hB)
            #Debugging:print(caseOutput)

            if controlOutput > caseOutput:
                result = 0

            else:
                result = 1

            if result == int(self.trainArray[t,casePos]):
                correct += 1

            else:
                incorrect += 1

            total +=1

        accuracy = (correct/float(total))
        return accuracy
                
                           
    
               
        
    #Create functions to get access to data
    def getAllData(self):
        return self.allData
    
    def getDataSample(self):
        return self.dataSample

    def getSampleArray(self):
        return self.sampleArray

    def getTrainArray(self):
        return self.trainArray




        
