from datetime import date
import requests

api_base_url_post = "https://api.megaventory.com/v2017a/json/reply"
api_key = "?APIKEY=59a80b0f6999f7a5@m103546"

salesID = []
salesType = set()
salesOrder = []


def productM():
    product_get = "/ProductGet"
    product_SKU = "&ProductSKU=1112256"
    endpoint_get_product = f"{api_base_url_post}{product_get}{api_key}{product_SKU}"
    req_product = requests.get(endpoint_get_product)

    if req_product.status_code in range(200, 299):
        data = req_product.json()
        results = data['mvProducts']
        product = []

        if len(results) > 0:
            for results in results:
                ID = results['ProductID']
                SKU = results['ProductSKU']
                Desc = results['ProductDescription']
                Sell = results['ProductSellingPrice']
                Purchase = results['ProductPurchasePrice']
                product.append(ID)
                product.append(SKU)
                product.append(Desc)
                product.append(Sell)
                product.append(Purchase)
            return product


def clientM():
    supplier_client_get = "/SupplierClientGet"
    client_filters = "&Filters=[{FieldName:SupplierClientType,SearchOperator:Equals,SearchValue:Client},{AndOr:And," \
                     "FieldName:SupplierClientName,SearchOperator:Equals,SearchValue:babis}]"
    endpoint_get_client = f"{api_base_url_post}{supplier_client_get}{api_key}{client_filters}"
    req_client = requests.get(endpoint_get_client)

    if req_client.status_code in range(200, 299):
        data = req_client.json()
        results = data['mvSupplierClients']
        client = []

        if len(results) > 0:
            for results in results:
                IDC = results['SupplierClientID']
                NameC = results['SupplierClientName']
                AddressBillingC = results['SupplierClientBillingAddress']
                AddressC = results['SupplierClientShippingAddress1']
                PhoneC = results['SupplierClientPhone1']
                EmailC = results['SupplierClientEmail']
                client.append(IDC)
                client.append(NameC)
                client.append(AddressBillingC)
                client.append(AddressC)
                client.append(PhoneC)
                client.append(EmailC)
            return client


def locationM():
    location_get = "/InventoryLocationGet"
    location_detail = "&Filters={FieldName:InventoryLocationName,SearchOperator:Equals,SearchValue:Main%20Location}"
    endpoint_get_location = f"{api_base_url_post}{location_get}{api_key}{location_detail}"
    req_loc = requests.get(endpoint_get_location)

    if req_loc.status_code in range(200, 299):
        data = req_loc.json()
        results = data['mvInventoryLocations']
        locations = []

        for results in results:
            IDL = results['InventoryLocationID']
            NameL = results['InventoryLocationName']
            AbbL = results['InventoryLocationAbbreviation']
            AddL = results['InventoryLocationAddress']
            locations.append(IDL)
            locations.append(NameL)
            locations.append(AbbL)
            locations.append(AddL)
        return locations


def taxM():
    tax_get = "/TaxGet"
    tax_filters = "&Filters=[{FieldName:TaxValue,SearchOperator:Equals,SearchValue:24},{AndOr:And,FieldName:TaxName," \
                  "SearchOperator:Equals,SearchValue:Sales}]"
    endpoint_get_tax = f"{api_base_url_post}{tax_get}{api_key}{tax_filters}"
    req_tax = requests.get(endpoint_get_tax)

    if req_tax.status_code in range(200, 299):
        data = req_tax.json()
        results = data['mvTaxes']
        tax = []

        if len(results) > 0:
            for results in results:
                IDT = results['TaxID']
                NameT = results['TaxName']
                ValueT = results['TaxValue']
                tax.append(IDT)
                tax.append(NameT)
                tax.append(ValueT)
            return tax


def discountM():
    discount_get = "/DiscountGet"
    discount_filters = "&Filters=[{FieldName:DiscountValue,SearchOperator:Equals,SearchValue:50},{AndOr:And," \
                       "FieldName:DiscountName,SearchOperator:Equals,SearchValue:Loyalty}]"
    endpoint_get_discount = f"{api_base_url_post}{discount_get}{api_key}{discount_filters}"
    req_dis = requests.get(endpoint_get_discount)

    if req_dis.status_code in range(200, 299):
        data = req_dis.json()
        results = data['mvDiscounts']
        discount = []

        if len(results) > 0:
            for results in results:
                IDD = results['DiscountID']
                NameD = results['DiscountName']
                DesD = results['DiscountDescription']
                ValueD = results['DiscountValue']
                discount.append(IDD)
                discount.append(NameD)
                discount.append(DesD)
                discount.append(ValueD)
            return discount


def salesM():
    sales_get = "/SalesOrderGet"

    endpoint_get_sales = f"{api_base_url_post}{sales_get}{api_key}"

    req_sales = requests.get(endpoint_get_sales)

    if req_sales.status_code in range(200, 299):
        data = req_sales.json()
        results = data['mvSalesOrders']

        for results in results:
            IDS = results['SalesOrderId']
            TypeS = results['SalesOrderTypeId']
            OrderNo = results['SalesOrderNo']
            salesID.append(IDS)
            salesType.add(TypeS)
            salesOrder.append(int(OrderNo))


def purchaseM(salesID, salesType, salesOrder, product, tax, client, discount, location):
    salesID.sort()
    nextID = salesID[len(salesID) - 1] + 1

    TypeID = salesType.pop()

    salesOrder.sort()
    nextNo = salesOrder[len(salesOrder) - 1] + 1

    date_now = date.today()

    amount = 2

    total = float(amount) * product[3]

    with_tax_total = total * int(tax[2]) / 100 + total

    total_tax = with_tax_total - total
    total_tax = "{:.2f}".format(total_tax)

    with_discount = with_tax_total - with_tax_total * int(discount[3]) / 100
    with_discount = "{:.2f}".format(with_discount)

    total_discount = float(with_tax_total) - float(with_discount)
    total_discount = "{:.2f}".format(total_discount)

    sales_update = "/SalesOrderUpdate"

    sales_details = "&mvSalesOrder={SalesOrderId:" + str(nextID) + ",SalesOrderTypeId:" + str(TypeID) + \
                    ",SalesOrderTypeAbbreviation:SO,SalesOrderTypeDescription:Sales Order,SalesOrderNo:" + \
                    str(nextNo) + ",SalesOrderDate:" + str(date_now) + ",SalesOrderCurrencyCode:EUR,SalesOrderClientID:" \
                    + str(client[0]) + ",SalesOrderClientName:" + str(client[1]) + ",SalesOrderBillingAddress:" + \
                    str(client[2]) + ",SalesOrderShippingAddress:" + str(
        client[3]) + ",SalesOrderInventoryLocationID:" + str(location[0]) + ",SalesOrderTotalQuantity:" \
                    + str(amount) + ",SalesOrderAmountSubtotalWithoutTaxAndDiscount:" + str(total) + \
                    ",SalesOrderAmountTotalDiscount:" + str(total_discount) + \
                    ",SalesOrderAmountTotalTax:" + str(total_tax) + ",SalesOrderAmountGrandTotal:" + str(
        with_discount) + \
                    ",SalesOrderDetails:[{SalesOrderRowDetailID:" + str(115) + ",SalesOrderRowProductID:" + str(
        product[0]) + \
                    ",SalesOrderRowProductSKU:" + str(product[1]) + ",SalesOrderRowProductDescription:" + str(
        product[2]) + \
                    ",SalesOrderRowQuantity:" + str(amount) + ",SalesOrderRowUnitPriceWithoutTaxOrDiscount:" + str(
        total) + \
                    ",SalesOrderRowTaxID:" + str(tax[0]) + ",SalesOrderTotalTaxAmount:" + str(int(tax[2])) + \
                    ",SalesOrderRowDiscountID:" + str(discount[0]) + ",SalesOrderRowTotalDiscountAmount:" + str(
        total_discount) + \
                    ",SalesOrderRowTotalAmount:" + str(with_discount) + "}],SalesOrderStatus:Verified," \
                                                                        "SalesOrderCreationDate:" + str(
        date_now) + "}&mvRecordAction=Insert"

    endpoint_update_sale = f"{api_base_url_post}{sales_update}{api_key}{sales_details}"

    req_purchase = requests.get(endpoint_update_sale)

    if req_purchase.status_code in range(200, 299):
        return nextID


if __name__ == '__main__':
    product = productM()
    location = locationM()
    tax = taxM()
    client = clientM()
    discount = discountM()
    salesM()

    if len(product) > 0 and len(tax) > 0 and len(client) > 0 and len(discount) > 0 and len(location) > 0:
        ID = purchaseM(salesID, salesType, salesOrder, product, tax, client, discount, location)

        sales_get = "/SalesOrderGet"

        sales_details = "&Filters={FieldName:SalesOrderID,SearchOperator:Equals,SearchValue:}" + str(ID)
        endpoint_get_sales = f"{api_base_url_post}{sales_get}{api_key}{sales_details}"
        req_sale = requests.get(endpoint_get_sales)

        if req_sale.status_code in range(200, 299):
            data = req_sale.json()
            results = data['mvSalesOrders']
            detail = results['SalesOrderDetails']

            print(results['SalesOrderClientName'] + " bought " + results['SalesOrderTotalQuantity'] + " piece of " + product[2] +
                  " for " + results['SalesOrderAmountGrandTotal'] + " at " + results['SalesOrderDate'])
