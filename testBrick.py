import brick

UPC = '088004027742'
ZIP = ['85031', '85033', '85037','85301', '85302', '85303', '85304', '85305', '85306', '85307', '85308', '85309', '85310', '85335', '85340', '85345', '85355', '85381', '85382',
 '85383', '85302', '85303', '85305', '85306', '85307', '85308', '85310', '85342', '85345', '85351', '85361', '85373', '85381', '85382', '85383', '85387']
STORES = ['Walmart', 'Target']
OUTPUT_FILE = 'testData'


#example for checking 1 zipcode
brick.Checker(UPC, '85310', STORES, OUTPUT_FILE)


#example for checking all the zipcodes in a list
for z in ZIP:

  brick.Checker(UPC, z, STORES, OUTPUT_FILE)
