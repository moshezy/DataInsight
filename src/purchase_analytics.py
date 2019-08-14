#'''
#
#            InsightDataScience/Purchase-Analytics Code Challenge
#                Submitted by Moshe Zychlinski
#
#'''
#!/usr/bin/python

import sys
import urllib.request
import requests
import csv
import operator

#select the run mode of excecution
#T1 = Test_1, T2 = Test_2, P = Production
run_mode = 'P'

#repo URL
repo_url = 'moshezy/DataInsight/master/'

#test_1 input URL
test_1_order_products_input = 'insight_testsuite/tests/test_1/input/order_products.csv'
test_1_products_input = 'insight_testsuite/tests/test_1/input/products.csv'

#test_2 input URL
test_2_order_products_input = 'insight_testsuite/tests/test_2/input/order_products.csv'
test_2_products_input = 'insight_testsuite/tests/test_2/input/products.csv'

#production input URL
order_products_input = 'input/order_products.csv'
products_input = 'input/products.csv'

#test_1 input files URL
test_1_order_products_url = 'https://raw.githubusercontent.com/' + repo_url + test_1_order_products_input
test_1_products_url = 'https://raw.githubusercontent.com/' + repo_url + test_1_products_input

#test_2 input files URL
test_2_order_products_url = 'https://raw.githubusercontent.com/' + repo_url + test_2_order_products_input
test_2_products_url = 'https://raw.githubusercontent.com/' + repo_url + test_2_products_input

#production input files URL
order_products_url = 'https://raw.githubusercontent.com/' + repo_url + order_products_input
products_url = 'https://raw.githubusercontent.com/' + repo_url + products_input

#output file URL
test_1_report_url = 'https://raw.githubusercontent.com/' + repo_url + 'insight_testsuite/tests/test_1/output/report.csv'
test_2_report_url = 'https://raw.githubusercontent.com/' + repo_url + 'insight_testsuite/tests/test_2/output/report.csv'
report_url = 'https://raw.githubusercontent.com/' + repo_url + 'output/report.csv'

#define input files by run mode

if run_mode == 'T1':
    order_products_url = test_1_order_products_url
    products_url = test_1_products_url
    report_url = test_1_report_url
elif run_mode == 'T2':
    order_products_url = test_2_order_products_url
    products_url = test_2_products_url
    report_url = test_2_report_url

#read order products csv from URL
#loop on order_products_data
#for each order:
    #read products csv from URL
    #convert each line in order products to string (list)
    #find product_id
    #loop on products to find if the product id from the order exist as product id in products
    #if exist add a new row (with relvant data for calculate report) to temp_report.csv
order_products_data = urllib.request.urlopen(order_products_url)
for order in order_products_data:
    order1 = order.strip()
    products_data = urllib.request.urlopen(products_url)
    order_data = str(order1).split(',')
    order_product_id = order_data[1]
    if order_product_id == 'product_id':
        continue
    for product in products_data:
        product1 = product.strip()
        product_data = str(product1).split(',')
        product_product_id = product_data[0].strip("b'")
        if product_product_id == 'product_id':
            continue
        if order_product_id == product_product_id:
            row = product_data[3].strip("'"), order_product_id, order_data[0].strip("b'"),order_data[3].strip("'")
            temp_report = open("temp_report.csv", "a")
            writer = csv.writer(temp_report)
            writer.writerow(row)
#open temp_report.csv for reading
temp_report2 = open("temp_report.csv", "r")
report_data = csv.reader(temp_report2, delimiter=",")
#sort file by department_id
sortedlist = sorted(report_data, key=operator.itemgetter(0),reverse=True)
#calculate the number of orders and number of first order for each department
#create full_report.csv
for i in range(len(sortedlist)):
    number_of_orders=1
    department_id = sortedlist[i][0]
    j = i+1
    number_of_first_orders = 0
    if sortedlist[i][3] == '0':
        number_of_first_orders = number_of_first_orders+1
    for j in range(j, len(sortedlist)):
        next_department_id = sortedlist[j][0]
        if department_id == next_department_id:
            number_of_orders=number_of_orders+1
            if sortedlist[j][3] == '0':
                number_of_first_orders = number_of_first_orders+1
    percentage = round(number_of_first_orders/number_of_orders, 2)
    full_report_row = department_id, number_of_orders, number_of_first_orders,percentage
    full_report = open("full_report.csv", "a")
    writer = csv.writer(full_report)
    writer.writerow(full_report_row)


report = {'file': open('full_report.csv', 'rb')}
r= requests.post(report_url, files=report) 

temp_report.close()
full_report.close()

#'''
#I couldn't delete duplicate rows with the same department_id
#delete duplicate rows from full_report.csv with the same department_id and create report.csv
#full_report = open("full_report.csv", "r")
#full_report_data = full_report.readlines()
#k = 1
#report = open("report.csv", "a")
#writer = csv.writer(report)
#for line in full_report_data:
#    if k > len(full_report_data):
#        break
#    currentline = full_report_data[k-1]
#    nextline = full_report_data[k]
#    if currentline.split(',')[0] == nextline.split(',')[0]:
#        writer.writerow(line)
#        k = k+1
#        continue
#'''
