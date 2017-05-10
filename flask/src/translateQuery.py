import pandas as pd 

def extractFieldnames(query):
	fieldnames = []
	values = query.split("@")[1:]
	for value in values:
		fieldname = value.split("#")[0]
		fieldnames.append(fieldname)
	return fieldnames

#read in the dictionary
dictionary = pd.read_csv("../dict/CollegeScorecardDataDictionary.csv")
#print dictionary["developer-friendly name"].head()
#print dictionary
query = "@average#[gte:1000] @sat#[lte:1200]"
fieldnames = extractFieldnames(query)
potential_fields = []
#print dictionary["VARIABLE NAME"].head()
friendlyNames = dictionary["developer-friendly name"]
variableNames = dictionary["VARIABLE NAME"]
for field in fieldnames:
	j = 0
	for i, row in dictionary.iterrows():
		#print(i)
		#print friendlyNames[i]
		if field in str(friendlyNames[i]):
			if not variableNames[i] in potential_fields:
				j = j + 1
				potential_fields.append(variableNames[i])
			if j==5: #adding a limit
				break
			#print(potential_fields)
print(potential_fields)