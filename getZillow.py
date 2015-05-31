# Author: Benjamin Wireman
# Date: 03/15/2015
# Objective: The goal of this program is to demonstrate the ability to mine data.

from lxml import html, etree
import numpy as np
import os

requestResult = open('results_zillow.xml', 'w')
file = open('Housing_Data.txt', 'w')
file.write("Data retrieved from http://www.zillow.com/homes/Warner-Robins-GA_rb/.\n\n")
#file.write("Data retrieved from http://www.zillow.com/homes/for_sale/Madison-County-AL/1894_rid/days_sort/34.920282,-85.860214,34.548984,-87.186813_rect/9_zm/1_p/1_rs/1_fr/.\n\n")

pageCount = 1
pg = 0
#for pg in range(pageCount):
pgStr = '%d/_p'
#page = html.parse('http://www.zillow.com/homes/Warner-Robins-GA_rb/')
page = html.parse('http://www.zillow.com/homes/for_sale/Madison-County-AL/1894_rid/days_sort/34.920282,-85.860214,34.548984,-87.186813_rect/9_zm/'+('%d_p' % (pg+1))+'/1_rs/1_fr/')

streetAddress = [td.text_content() for td in page.xpath('//dt[@class="property-address"]//a')]
price = [td.text_content() for td in page.xpath('//div//dt[@class="price-large zsg-h2 zsg-content_collapsed"]')]
#houseInfo = [td.text_content() for td in page.xpath('//div//dt//span[@class="beds-baths-sqft"]')]
#lotInfo = [td.text_content() for td in page.xpath('//div//dt//span[@class="lot-size"]')]
#lifeSpanOnZillow = [td.text_content() for td in page.xpath('//div//dt[@class="doz zsg-fineprint"]')]

address = np.array(streetAddress)

print streetAddress

for i in range(len(streetAddress)):
    if "Plan" not in streetAddress[i]:
        addr = ""
        citystatezip = ""
        data = ""
        for j in range(len(streetAddress[i])):
            if streetAddress[i][j] != ",":
                addr = addr + streetAddress[i][j]
            else:
                citystatezip = streetAddress[i][j+2:-1] + streetAddress[i][-1]
                break
        address[i] = addr + ", " + citystatezip
#    print addr + ", " + citystatezip + ", " + price[i]

"""Go through the data and convert it to needed data types."""
for i in range(len(streetAddress)):
    if "Plan" not in streetAddress[i]:
        newPrice = ""
        converted = np.array(price)
        for j in range(len(price[i])):
            if price[i][j] is not "$" and price[i][j] is not "," and price[i][j] is not "+" and price[i][j] is not "/" and price[i][j] is not "m" and price[i][j] is not "o" and price[i][j] is not "N" and price[i][j] is not "A" and price[i][j] is not "f" and price[i][j] is not "r" and price[i][j] is not "k" and price[i][j] is not "K" and price[i][j] is not ' ' and price[i][j] is not '':
                newPrice = newPrice + price[i][j]
        price[i] = newPrice

"""Sort the data."""
#    print price
sortedPrices = np.array(price)
#sortedPrices = np.sort(sortedPrices)
index = np.empty(5)
count = 0
for k in range(len(sortedPrices)):
    if sortedPrices[k] == "":
        index[count] = k
        count += 1
sortedPrices = np.delete(sortedPrices, index, None)


#    file.write(str(i+1) + ": " + addr + ", " + citystatezip + "\n")
#    data = html.parse('http://www.zillow.com/webservice/GetDeepSearchResults.htm?zws-id=X1-ZWz1ahswkuy6tn_a1050&' + (('address=%s') % addr) + (('&citystatezip=%s') % citystatezip))
#    result = etree.tostring(data, pretty_print=True, method="xml")
#    requestResult.write(result)
#    error = [comps.text_content() for comps in data.xpath('//message//code')]
#    errorMsg = [comps.text_content() for comps in data.xpath('//message//text')]
#    if error[0] == "7":
#        print errorMsg, error
#        quit()
#    zpid = [pid.text_content() for pid in data.xpath('//zpid')]
#    print zpid
#    if zpid:
#        print zpid[0]
#        data = html.parse('http://www.zillow.com/webservice/GetDeepComps.htm?zws-id=X1-ZWz1ahswkuy6tn_a1050&'+ (('zpid=%s') % zpid[0]) +'&count=25')
#        result = etree.tostring(data, pretty_print=True, method="xml")
#        requestResult.write(result)
#        error = [comps.text_content() for comps in data.xpath('//message//code')]
#        errorMsg = [comps.text_content() for comps in data.xpath('//message//text')]
#        if error[0] == "503" or error[0] == "500":
#            print errorMsg, error
#        else:
#            compsAddress_Street = [comps.text_content() for comps in data.xpath('//comparables//address//street')]
#            compsAddress_Zip = [comps.text_content() for comps in data.xpath('//comparables//address//zipcode')]
#            compsAddress_City = [comps.text_content() for comps in data.xpath('//comparables//address//city')]
#            compsAddress_State = [comps.text_content() for comps in data.xpath('//comparables//address//state')]
#            compsAssessment_Year = [comps.text_content() for comps in data.xpath('//comparables//taxassessmentyear')]
#            compsAssessment_Price = [comps.text_content() for comps in data.xpath('//comparables//taxassessment')]
#            compsLastSold_Date = [comps.text_content() for comps in data.xpath('//comparables//lastsolddate')]
#            compsLastSold_Price = [comps.text_content() for comps in data.xpath('//comparables//lastsoldprice')]
#            for l in range(len(compsAddress_Street)):
#                compsAddress = [compsAddress_Street[l] + " " + compsAddress_City[l] + " " + compsAddress_State[l] + " " + compsAddress_Zip[l]]
#                compsAssessment = [compsAssessment_Year[l] + " " + compsAssessment_Price[l]]
#                compsLastSold = [compsLastSold_Date[l] + " " + compsLastSold_Price[l]]
#                file.write(compsAddress[0] + ", " + compsAssessment[0] + ", " + compsLastSold[0] + str("\n"))
#                file.write(compsAssessment[0] + ", " + compsLastSold[0] + str("\n"))
print price, str("\n--------------------------------------------------------------------------------\n\n")


"""Compare the prioritized data with relevant data corresponding to houses around it."""
sortedPrices = sortedPrices.astype(np.float)
flagged = range(0,len(sortedPrices))
for i in range(len(sortedPrices)):
    if sortedPrices[i] >= 10000.0 and sortedPrices[i] < 50000.0:
        flagged[i] = streetAddress[i] + ", " + str(sortedPrices[i])
        sendText = "curl -X POST https://api.twilio.com/2010-04-01/Accounts/ACae9ccfd5a85ee5e105dd705fbf880838/SMS/Messages.json \
        -u ACae9ccfd5a85ee5e105dd705fbf880838:5e51c22abc4cfd70f1b24c0b9de75e3f \
        --data-urlencode \"From=+12077473812\" \
        --data-urlencode \"To=+12563483346\" \
        --data-urlencode \'Body=%s\'" % str(flagged[i])
        os.system(sendText)
    elif sortedPrices[i] >= 50000.0 and sortedPrices[i] < 80000.0:
        flagged[i] = streetAddress[i] + ", " + str(sortedPrices[i])
    else:
      flagged[i] = streetAddress[i] + ", " + str(sortedPrices[i])
    file.write(str(flagged[i]) + str("\n \n"))
print str("\n--------------------------------------------------------------------------------\n\n")