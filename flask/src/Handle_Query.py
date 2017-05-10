helpMessage = "The \'@\' symbol starts each field search, and is followed by the field you want to search in \nThe \'#\' symbol starts the list of values that you expect to find in the field\nIf you expect a numeric field, the the upper and lower bound of values must be specified.\n To specify the bounds, the following conditions can be used\n a) gte - greater than or equal to\n b) lte - less than or equal to\n c) gt - greater than\n d) lt - less than\nLastly, sperate successive terms inside the \'[..]\' by a comma"
queryOperators = [] #this is the store the operators used in the query to test if it defines the proper boundaries
    #Check to see if the operator is valid
#fucntion that parses the query
def parseQuery(query):
    searchType = None
    #first check the number of @ symbols in the query
    fields = query.split("@")
    #print(fields)
    bool_count = 0;
    range_count = 0;
    print(fields)
    if len(fields) > 1:
        #type of search can either be multi_range or mixed
        for field in fields:
            inputValues = field.split("#")
            print(inputValues)
            fieldname = inputValues[0]
            arguments = inputValues[1].replace("[","").replace("]","")
            args = arguments.strip(" ").split(",")
            #print(args)
            for arg in args:
                #print(arg)
                #arg = arg.strip(" ")
                #print(arg)
                argfields = arg.strip(" ").split(":")
                #print(argfields)
                if len(argfields) == 1:
                    #boolean search
                    bool_count = bool_count + 1
                elif len(argfields) == 2:
                    #range search
                    #check to see that there are two values for the range search
                    if len(args) > 2:
                        #print(len(args))
                        printError("A range query should have no more than 2 arguments to set the bounds")
                    checkProperRange(argfields)
                    range_count = range_count + 1 #this is not the case. Test to see if the name is the argument is valid
                    #TODO: Check to see if the arguments are valid
                else:
                    #this is an error
                     printError("This is improper syntax")
            #check the operators used in the query to make sure that the bounds of the range search are properly defined
            checkProperOps()
        if(bool_count != 0 and range_count != 0):
            searchType = "mixed"
        elif(bool_count != 0 and range_count == 0):
            searchType = "bool"
        elif(bool_count == 0 and range_count != 0):
            searchType = "multi_range"
    else:
        #type of search can either be single rangle of bool
        #it will be bool if there is no detection of any of the keywords
        inputValues = query.split("#")
        fieldname = inputValues[0]
        arguments = inputValues[1].replace("[", "").replace("]", "")
        args = arguments.strip(" ").split(",")
        for arg in args:
            argfields = arg.strip(" ").split(":")
            if len(argfields) == 1:
                #searchType = "bool"
                bool_count = bool_count + 1
            elif len(argfields) == 2:
                #check to see that there are two values for the range search
                if len(args) > 2:
                    printError("A range query should have no more than 2 arguments to set the bounds")
                #Check to see if the operator is valid
                checkProperRange(argfields)
                range_count = range_count + 1
            else:
                printError("This is improper syntax")
        #check the operators used in the query to make sure that the bounds of the range search are properly defined
        checkProperOps()
        #determine the search type
        if bool_count != 0 and range_count != 0:
            printError("Field search cannot contain a range and a value")
        elif bool_count != 0:
            searchType = 'bool'
        elif range_count != 0:
            searchType = 'single_range'
        else:
            printError("It shouldn't have come to this")
    #print(bool_count)
    #print(range_count)
    print(searchType)
    if searchType == None:
        printError("Could not determin the type of search")
    result = []
    if searchType=='bool' or searchType=='single_range':
        result.append("data/%s"%(query))
    else:
        newQuery = query.replace("@","data/") #I am not sure if this is what we want to pass
        result.append("data/%s"%(newQuery))
    result.append(searchType)
    return result

def printError(message):
    print("ERROR: %s\n"%(message))
    print(helpMessage)
    quit()

def checkProperRange(argfields):
    keywords = ["lte","gte","lt","gt"]
    valid = False
    #print(argfields[0])   
    #clear the queryOperators list
    #queryOperators[:] = []
    for op in keywords:
        if op == argfields[0].strip(" "):
            valid = True
            queryOperators.append(op)
            break
    if not(valid):
        printError("Unknown comparison operator '%s'"%(argfields[0].strip(" ")))
    #the second value should be a numeric value
    if not(argfields[1].isdigit()):
        printError("Range values must be numeric")


def checkProperOps():
    if len(queryOperators) != 0:
        if len(queryOperators) > 2: #shouldn't need this, but just to double check
            printError("A range query should have no more than 2 arguments to set the bounds") 
        if len(queryOperators) == 1: #this does not need to be checked
            return
        if queryOperators[0] == queryOperators[1]:
            printError("Cannot define the same bound twice")
        if queryOperators[0] == "lt" or queryOperators[0] == "lte":
            if queryOperators[1] != "gte" and queryOperators[1] != "gt":
                printError("Bounds of the range search are not properly defined")
        elif queryOperators[0] == "gt" or queryOperators[0] == "gte":
            if queryOperators[1] != "lte" and queryOperators[1] != "lt":
                printError("Bounds of the range search are not properly defined")
                
                
#===============================================================
# 
#===============================================================

def parseQuery2(raw_query):
    '''
    '''
    search_type = None
    preProcess_query = raw_query
    #check if it is a boolean search, field search, or phrase search
    if "@" in raw_query:
        search_type = 'mixed'
    elif "p:" in raw_query:
        search_type = 'phrase'
    else :
        search_type = 'bool'
    
    if search_type == 'mixed':
        preProcess_query = raw_query.replace("@", "data/")
    elif search_type == 'phrase':
        preProcess_query = raw_query.replace("p:", "")
    
    return (preProcess_query,search_type)

def parseQuery3(raw_query):
    '''
    '''
    search_type = None
    preProcess_query = raw_query
    #check if it is a boolean search, field search, or phrase search
    if "@" in raw_query:
        search_type = 'mixed'
        #check the format of the query
        fields = raw_query.split("@")
        fields = fields[1:]
        #print(fields)
        for field in fields:
            sections = field.split("#")
            if len(sections) != 2:
                printError("Syntax Error")
            fieldname = sections[0]
            values = sections[1].strip(" ")
            #print(fieldname)
            #print(values)
            #check the brackets in values
            if values[0] != '[' or values[len(values)-1] != ']':
                printError("Missing brackets")
            elif values.count(']') != 1:
                printError("Syntax error: Too many ']' ")
            values = values.replace("[", "").replace("]","")
            values = values.split(",")
            for value in values:
                x = value.split(":")
                if len(x) == 2:
                    #check the range
                    checkProperRange(x)
                    checkProperOps()
                elif len(x) == 1:
                    continue
                else:
                    printError("Syntax error -- too many ':' ")
            queryOperators[:] = []
            #print fieldname
            #print values
    elif "p:" in raw_query:
        search_type = 'phrase'
    else :
        search_type = 'bool'
    
    if search_type == 'mixed':
        preProcess_query = raw_query.replace("@", "data/")
    elif search_type == 'phrase':
        preProcess_query = raw_query.replace("p:", "")
    
    return (preProcess_query,search_type)
        