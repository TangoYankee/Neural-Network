##Written By Tim Miller
##Professor Land
##02/15/2012





#Import libraries
import math 
import numpy
import random


#Define the class
class neuralNetwork:
    #Construct the variables to be called and manipulated
    def __init__(self):

        self.__INPUTS = numpy.array([(0,0),(1,0),(0,1),(1,1)])
        self.__numPairs = 4
        self.__TRUEVALUES = (0,1,1,0)

        self.__N_ONE = .5
        self.__N_TWO = .1
        

        #self.__crrntHddnWeights = self.initialElements(4, "weight").reshape(2,2)
        #self.__crrntOutWeights = self.initialElements(2,"weight")
        #self.__crrntBiasHddn = self.initialElements(2,"bias")
        #self.__crrntBiasOut = self.initialElements(1,"bias")

        #Lecture values reduced by 30%. These are the values that are seen in
        #the graph
        self.__crrntHddnWeights = numpy.array([(-3.36, 3.22),(3.57, -3.64)]) 
        self.__crrntOutWeights = numpy.array([4.13, 3.64]) 
        self.__crrntBiasHddn = numpy.array([(1.82), (2.52)])
        self.__crrntBiasOut = numpy.array([1.89])

        #Observed and IValues for All training Pairs
        self.__allObservedValues = list()
        self.__allIValues = list()

        #Observed and IValues for most inaccurate training pair
        self.__singleObservedValue = 0
        self.__singleIValues = list()

        #Most Inaccurate Pair
        self.__mostInaccuratePair = 0

        #Squared Difference Values
        self.__SDValue = 0
        self.__SDValueAll = list()

        
        #Define the training pairs and the threshold value
        self.__thresholdValue = 0.05



    #Operator Functions

    #Function to go through feed forward process
    def feedForwardAll(self):
        
        #Create empty list to collect values of interest
        observedValues = list()
        IValues = list()

        #Create a for loop to go through all the necessary training pairs
        for i in range(self.__numPairs):

            #Calculate the Hidden layer
            inputToHidden = (numpy.dot(self.__crrntHddnWeights, self.__INPUTS[i])-self.__crrntBiasHddn)

            outputOfHiddenLst = list()
            for t in range(len(inputToHidden)):
                outputOfHiddenLst.append(1/(1+math.exp(-inputToHidden[t])))

            #Record the I Values in order to use them in back prapogation 
            IValues.append(outputOfHiddenLst)

            #Calculate the Output Layer
            inputToOutLayer = numpy.array(outputOfHiddenLst)

            preSigmoidOutput = (numpy.dot(self.__crrntOutWeights, inputToOutLayer)-self.__crrntBiasOut)
            finalOutput = 1/(1+math.exp(-preSigmoidOutput))

            #Recored the outputs for all the training pairs
            observedValues.append(finalOutput)

        #Reset the I values and Output Values
        self.__allObservedValues = observedValues
        self.__allIValues = IValues



    def feedForwardSingle(self):

            #Calculate the Hidden layer
            inputToHidden = (numpy.dot(self.__crrntHddnWeights, self.__INPUTS[self.__mostInaccuratePair])-self.__crrntBiasHddn)

            outputOfHiddenLst = list()
            for t in range(len(inputToHidden)):
                outputOfHiddenLst.append(1/(1+math.exp(-inputToHidden[t])))

            #Calculate the Output Layer
            inputToOutLayer = numpy.array(outputOfHiddenLst)

            preSigmoidOutput = (numpy.dot(self.__crrntOutWeights, inputToOutLayer)-self.__crrntBiasOut)
            finalOutput = 1/(1+math.exp(-preSigmoidOutput))

            #Recored the final output and IValues
            self.__singleObservedValue = finalOutput #Number
            self.__singleIValues = outputOfHiddenLst #List


        


            





    
    #Create a function to perform back propagation which takes the output and I values of interest
    def backPropagation(self):

        #Take the inputs for the given training pair
        inputsProp = self.__INPUTS[self.__mostInaccuratePair]
       

        #Calculate the change in the output layer
        dOutput = (self.__TRUEVALUES[self.__mostInaccuratePair] - self.__singleObservedValue)*(self.__singleObservedValue)*(1-self.__singleObservedValue)

        #Calculate the change in I values of Hidden layer
        changeInIofHidden = list()
        for i in range(len(self.__singleIValues)):

            changeInIofHidden.append(self.__singleIValues[i]*(1-self.__singleIValues[i])*self.__crrntOutWeights[i]*dOutput)

        #Find the value by which to adjust the hidden weights
        hiddenWeightMasterList = list()
        for t in range(len(changeInIofHidden)):

            hiddenWeightSlaveList = list()
            for i in range(len(inputsProp)):
                
                hiddenWeightSlaveList.append(changeInIofHidden[t]*inputsProp[i]*self.__N_ONE)
            hiddenWeightMasterList.append(hiddenWeightSlaveList)
            
        hiddenUpdater = numpy.array(hiddenWeightMasterList)

        #Update the Hidden Weights
        updatedHiddenWeight = self.__crrntHddnWeights + hiddenUpdater
    

        #Update the hidden layers biases
        updatedHiddenBias = (self.__crrntBiasHddn-numpy.array(changeInIofHidden)*self.__N_ONE)
    

        #Update the output weights 
        outWeightMasterList = list()
        for i in range (len(self.__singleIValues)):
            updateOutLayer = self.__crrntOutWeights[i]+(self.__singleIValues[i]*self.__N_TWO*dOutput)
            outWeightMasterList.append(updateOutLayer)
        updatedOutWeights = numpy.array(outWeightMasterList)

        #Update the Output Biases
        updatedOutputBias = (self.__crrntBiasOut-((self.__N_TWO)*dOutput))

        #Update the attributes of the object to reflect the new weights and biases
        self.__crrntHddnWeights = updatedHiddenWeight
        self.__crrntOutWeights = updatedOutWeights
        self.__crrntBiasHddn = updatedHiddenBias
        self.__crrntBiasOut = updatedOutputBias
        

    



    #Define a function to take the squared difference which takes the training pair of interest and its observed values
    def squaredDifferenceAll(self):

        #create a list to collect values
        differenceList = list()


        for i in range(self.__numPairs):
            #subtract the observed value from the true value
            difference = self.__TRUEVALUES[i]- self.__allObservedValues[i]
            #square their difference
            instance = math.pow(difference,2)
            #record the result
            differenceList.append(instance)

        self.__SDValueAll = differenceList
        self.__SDValue = max(self.__SDValueAll)




    def squaredDifferenceSingle(self):

        difference = self.__TRUEVALUES[self.__mostInaccuratePair]- self.__singleObservedValue
        self.__SDValue = math.pow(difference, 2)

            



        
    #Define a function to give the values of the weights, biases, and squared differences
    def getHddnWeights(self):
        return self.__crrntHddnWeights

    def getOutWeights(self):

        return self.__crrntOutWeights,

    def getHddnBias(self):
        return self.__crrntBiasHddn

    def getOutBias(self):

        return self.__crrntBiasOut

    def getSDValueAll(self):

        return self.__SDValueAll
        
    




    #User defined function to initialize the weights and biases
    def initialElements (self,elements, which):

        #Create an empty list to record the values 
        totalList = list()

        #If we are creating values for weights, allow for the possibility of negative values
        if which == "weight":

            #create a for loop that will add the desired number of elements to the list
            for i in range (elements):
                #Randomly generate a number between 5.5 and 10. Then, multiply it by 1 or -1
                totalList.append(random.uniform(5.5, 10)*random.sample((1,-1),1)[0])       

        else:
            for i in range(elements):
                #Generate a random number between 5.5 and 10. Only let it be positive 
                totalList.append(random.uniform(10, 5.5))

        #Turn the list into a matrix
        totalArray = numpy.array(totalList)

        #Return the created matrix
        return totalArray









    #Define a run function to handle the logic of the code
    def run(self):


        #Create a blank file to record the squared difference values as the least accurate training pair
        #is being trained
        #recordOfSD = open("SDs.csv", 'w')

        #Begin the Training process
        for i in range(1000):

            #Feed forward all four of the training Pairs
            self.feedForwardAll()

            #Find the squared differences for all four training pairs
            self.squaredDifferenceAll()

            #Select the training pair with the largest squared difference
            self.__mostInaccuratePair = (list.index(self.__SDValueAll,self.__SDValue))
            

            #Select the observed and I values for the most inaccurate training pair
            self.__singleIValues = self.__allIValues[self.__mostInaccuratePair]
            self.__observedValue = self.__allObservedValues[self.__mostInaccuratePair]

            #Run the least accurate training pair through back propagation until it reaches
            #thresold
            c = 0       
            while self.__SDValue > self.__thresholdValue and c<=1000:
            

                #Run the training pair through back propagation and update the weights and biases with new values
                self.backPropagation()

                #Feed Forward the single pair
                feedForwardResult = self.feedForwardSingle()

                #Determine the new squared differnce of the training pair
                self.squaredDifferenceSingle()
            
                #Write the SD value to a file
                #recordOfSD.write(str(self.__SDValue) + "\n")
                #Add to the counter to prevent an infinite loop
                c+=1
                #print(self.__SDValue)

            #Make the threshold value more strict
            self.__thresholdValue = self.__thresholdValue * .95

        #Close the file which records the SD values
        #recordOfSD.close()






