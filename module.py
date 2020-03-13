import json


with open("C:/Users/nasser/finalyear/api/Ally.json", "r") as read_file:
    data = json.load(read_file)
print("Hello world!!\n")

uniqueNames = []
for i in data["_via_img_metadata"]:
    if(i not in uniqueNames):
        uniqueNames.append(i)
    
print(len(uniqueNames))

count = 0
for name in uniqueNames:
    for region in data['_via_img_metadata'][name]['regions']:
        print('\n')
        print(data['_via_img_metadata'][name]['filename'])
        if "Disease_1" in region['region_attributes']:
            for disease in region['region_attributes']:
                count += 1
                print(region['region_attributes']['Disease_1'])
        else:
            print("Fuck off mate!!")
        
print(count)