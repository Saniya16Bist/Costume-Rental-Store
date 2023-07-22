from datetime import date

def main():
    print("~~"*30)
    print("\tWelcome to costume Rental Application")
    print("\t\tDesigned by Saniya Bist")
    print("~~"*30)


def selection():
    print("Please select your desirable option here :)\n")
    print("(1) Enter 1 to rent a costume\n")
    print("(2) Enter 2 to return a costume\n")
    print("(3) Enter 3 to exit from the application\n")


def exitMessage():
    print("\nThank You for using our application.")
    print("\nPlease visit again :).")


def invalid():
    print("Invalid option")
    print("\nPlease provide the valid option.\n")


def updateDB(costumes):
    # clean
    open('./costume.txt', 'w').close()
    # write
    file = open('./costume.txt', 'a')
    for e in costumes["items"]:
        line = f"{e['name']}, {e['brand']}, ${e['price']}, {e['quantity']}\n"
        file.write(line)
    file.close()


def save_invoice(customer_name, invoice):
    # save invoice
    filename = customer_name + '_' + str(date.today())+'.txt'
    file_path = f'./invoices/{filename}'
    file = open(file_path, 'w')
    file.write(invoice.replace('\t', ''))
    file.close()
    print("\t\t Costume rent successful.\n")
    print('~~'*40+'\n')


def updateQty(invoice, customer_name, costume, buying_qty):
    # ask user to buy more quantity
    ans = input("Do you want to update quantity (yes or no) : ")
    if ans == 'yes':
        new_qty = qty(costume["quantity"])
        costume["quantity"] = costume["quantity"]-new_qty
        invoice = invoice_format(customer_name, costume, buying_qty+new_qty)
    return [invoice, costume, ans == 'yes']


def invoice_format(customer_name, costume, quantity):
    # format of an invoice
    bill = costume["price"] * quantity
    invoice = f'''\t\t\t Invoice
        \t Costume ID : {costume["id"]}
        \t Customer Name : {customer_name}
        \t Costume Name : {costume["name"]}
        \t Brand : {costume["brand"]}
        \t Date : {date.today()}
        \t Quantity : {quantity}
        \t Rate (5 days) : {costume["price"]}
        \t Total Amount ($) : {bill} /-
        '''
    return invoice


def show_invoice(invoice):
    print('--'*40)
    print(invoice)
    print('--'*40)


def invoice(costume, quantity):
    # show & save invoice
    customer_name = input("Enter customer fullname : ")
    invoice = invoice_format(customer_name, costume, quantity)
    show_invoice(invoice)
    [invoice, costume, updated] = updateQty(
        invoice, customer_name, costume, quantity)
    if updated:
        show_invoice(invoice)
    save_invoice(customer_name, invoice)
    return costume


def rent_costume(costumes):
    # rent costume, update quantity is needed, show invoice
    rentCostumeID = validateCostumeID(costumes["total"])
    costume = costumes["items"][rentCostumeID-1]
    stockQuantity = costume["quantity"]
    if stockQuantity > 0:
        print(f'\t Costume "{costume["name"]}" is available. :)')
        qty_cos = qty(stockQuantity)
        costume["quantity"] = stockQuantity-qty_cos
        #
        costume = invoice(costume, qty_cos)
        costumes[rentCostumeID-1] = costume
        updateDB(costumes)

def rent():
    file =open("stock.txt", "r")
    count = 0
    dic_costume = {}
    for line in file:
        count=count+1
        line=line.replace("\n","")
        line = line.split(',')
        
        dic_costume[count]=line

    #print(dic_costume)
    return dic_costume
    file.close()


def get_costumes():
    # load costumes from file as dictionary
    costumes = {"total": 0, "items": []}
    file = open("costume.txt", "r")
    count = 0
    for line in file:
        if not line.isspace():
            count = count + 1
            line = line.replace('\n', '').replace('\t', '').split(',')
            costumes["items"].append({
                "id": count,
                "name": line[0],
                "brand": line[1],
                "currency": "$",
                "price": float(line[2].replace('$', '').replace(' ', '')),
                "quantity": int(line[3])
            })
    costumes["total"] = count
    file.close()
    return costumes


def display_costumes(costumes=None):
    print("--"*40)
    print("ID \t Costume Name \t\t Brand \t\t Price \t\tQuantity")
    print("--"*40)
    for costume in costumes["items"]:
        print(
            f'{costume["id"]} \t {costume["name"]} \t {costume["brand"]} \t ${costume["price"]} \t\t {costume["quantity"]}')
        print("--"*40)


def validateCostumeID(totalCostumes):
    valid = int(input("\nEnter a costume id to rent a costume: "))
    if valid <= 0 or valid > totalCostumes:
        print("\nPlease enter valid ID !\n")
        validateCostumeID(totalCostumes)
    return valid


def qty(stockQuantity):
    # check if required quantity is available in stock
    qty_cos = int(input(f"\nEnter the quantity of selected costume: "))
    if qty_cos <= 0:
        print("\nPlease provide the valid quantity")
    elif qty_cos > stockQuantity:
        print("\nSorry, the qunatity is more than stock.")
    else:
        return qty_cos
    qty(stockQuantity)
    
def rent():
    file =open("costume.txt", "r")
    count = 0
    dic_costume = {}
    for line in file:
        count=count+1
        line=line.replace("\n","")
        line = line.split(',')
        
        dic_costume[count]=line

    print(dic_costume)
    return dic_costume
    file.close()


def read_invoice(filename):
    # read invoice of customer
    try:
        file = open('./invoices/'+filename, 'r')
        invoice = file.read()
    except Exception as e:
        print("\t Enter valid name or date!\n")
        return [None, None]
    # returns [invoice, rented_date]
    return [invoice, filename.replace('.', '_').split('_')[1]]


def validate_return_date(rented_date, input_date):
    # validate return date
    if input_date != rented_date:
        return False
    return True


def makefine(days):
    # calculate fine
    rate = int(input("Enter fine rate (per day) : "))
    _fine = rate*days
    return _fine


def extract_from_invoice(invoice):
    # extracts costumeID & rented_quantity from stored invoice
    lines = invoice.split('\n')
    ID = lines[1].split(':')[1]
    qty = lines[6].split(":")[1]
    return [int(ID), int(qty)]


def return_costume(filename, invoice, rented_days, costumes):
    # handle custom return functionality
    if rented_days > 5:
        print(f"\tCustomer delayed returning costume i.e. {rented_days} days")
        fine = makefine(rented_days)
        print(f"\t Customer is fined ${fine}\n")
        with open('./invoices/'+filename, 'a') as f:
            f.write(f'\t\tFine ($) : {fine}')
    [ID, qty] = extract_from_invoice(invoice)
    costumes["items"][ID-1]["quantity"] += qty
    updateDB(costumes)
    print("\tCostume returned successfully!\n")
    # just thanking customer : don't remove line below;
    exitMessage()
