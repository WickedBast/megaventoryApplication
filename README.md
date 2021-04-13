# megaventoryApplication

This project uses Megaventroy API to get its data. To able to do that, this "59a80b0f6999f7a5@m103546" key is used as APIKEY.

In productM method: This method makes a get request from API with a specific product's SKU value. If this request returns "OK", it adds necessary data of the product part to a list. Then, it returns this list.

In clientM method: This method makes a get request from API with a specific client's name and type values. If this request returns "OK", it adds necessary data of the client part to a list. Then, it returns this list.

In locationM method: This method makes a get request from API with a specific location's name value. If this request returns "OK", it adds necessary data of the location part to a list. Then, it returns this list.

In taxM method: This method makes a get request from API with a specific tax's amount and name values. If this request returns "OK", it adds necessary data of the tax part to a list. Then, it returns this list.

In discountM method: This method makes a get request from API with a specific discount's amount and name values. If this request returns "OK", it adds necessary data of the discount part to a list. Then, it returns this list.

In salesM method: This method makes a get request from API for all sales made until the current date. If this request returns "OK", it adds necessary data of the sale part to two different lists and a set defined at the start of the project.

In purchaseM method: This method gets many parameters that will be filled by previous methods to make the purchase. In this method, there are many calculations to calculate the final price, total tax amount, and total discount. Then, this method creates a new sale using all these data which has been collected by previous methods by requesting API. If this request returns "OK", it returns the SaleID. 

In the main method: This method executes productM, locationM, taxM, clientM, and discountM methods and gives those method's values to a list for each. Then, executes the salesM method and checks those lists have a value inside. If each of them has a value inside, it executes the purchaseM method and passes the value to a variable. The method makes a get request using this variable. If this request returns "OK", it prints the important details about the sale that have been made.
