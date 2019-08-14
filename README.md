# DataInsight - code chalange
# submitted by Moshe Zychlinski

instruction:
1. before running the code, you should chose the run mode (line 17 in src file)
   T1 = Test_1, T2 = Test_2, P = Production
2. right now the run mode is P = Production

code logic:
1. define variables for input and output destination
2. for each order product, find its product_id in product file
3. create temp report file with order information + product information (such as department_id)
4. from temp report file calculate data for the report file
5. delete duplicate lines with the same department_id (I couldn't implement this part)
6. save report file in its destination
7. close all open files


#thank you so much!
