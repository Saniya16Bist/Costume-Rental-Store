from funcs import *


if __name__ == "__main__":
    # greeting
    main()
    continueLoop = True
    while continueLoop:
        # show user options
        selection()
        value = int(input("\nEnter a desirable option: "))
        costumes = get_costumes()
        if value == 1:
            display_costumes(costumes)
            rent_costume(costumes)
        elif value == 2:
            # return costume
            print("\n\t [ Returning a costume ]")
            customer_name = input("Enter customer name : ")
            input_date = input("Enter rented date (yyyy-mm-dd) : ")
            # check date, date is more than 5 days ? fine : updateDB
            filename = customer_name+'_' + input_date + '.txt'
            [invoice, rented_date] = read_invoice(filename)
            if invoice:
                show_invoice(invoice)
                is_date_valid = validate_return_date(rented_date, input_date)
                try:
                    is_date_valid
                    [y, m, d] = rented_date.split('-')
                    rented_days = (
                        date.today() - date(int(y), int(m), int(d))).days
                    return_costume(filename, invoice, rented_days, costumes)
                except:
                    print("\t[!] Enter valid date!")
        elif value == 3:
            exitMessage()
            break
        else:
            invalid()
