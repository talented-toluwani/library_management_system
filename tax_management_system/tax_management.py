import json

def load_tax_brackets():
    """loads the json file, and handles any errors that might occurr while doing that  """
    try:
        with open("/home/edgalmiracle/python/tax_management_system/tax_bracket_2009.json", "r") as file:
            tax_data = json.load(file) #deserializies a json string to python dictionary or list
            return tax_data

    except FileNotFoundError:
         print("The 2009 tax file could not load. Please, ensure that the data file exists, and try again.")
         return None
    
    except UnicodeError:
        print("The file is not UTF-8 encoded")

    except json.JSONDecodeError:
        print("The contents of the file are not json format. ")
        return None


def get_user_filing_status():
    """a function that asks user for their filing status and validate whether it is in the given bracket"""
    while True:
        try:
           user_filing_status = int(input("Please enter in your filing status: "))

           if 0 <= user_filing_status <= 3:
               return user_filing_status
           
           else:
               print("User filing status must be between [0,1,2,3].")

        except ValueError:
            print("Invalid input. Please, re enter your filing status.")
    
def get_user_taxable_income():
    """prompts user for their taxable income, and handles any possible error that may occur in the process"""
    while True:
        try:
            user_taxable_income = float(input("Please enter in your taxable income: "))

            if user_taxable_income > 0:
                return user_taxable_income
            
            else:
                print("User taxable income must be greater than 0")

        except ValueError:
            print("Invalid input. Please re enter your taxable income.")

def get_tax_bracket(user_filing_status, tax_data):
    """this functions matches the users filing status to the appropraite tax bracket"""
    converted_user_filing_status = str(user_filing_status)#JSON dictionary keys are string, so it has to be converted

    tax_bracket_data = tax_data.get(converted_user_filing_status)
    return tax_bracket_data

def calculate_tax(tax_bracket_data, user_taxable_income):
    """this calculates the tax of the users based on the tax brackets and income bracket"""
    if tax_bracket_data is None:
        raise ValueError("Failed to get users filing data bracket from the file")
    
    total_tax = 0 
    
    for data_bracket in tax_bracket_data:
        if user_taxable_income <= data_bracket["min"]:
            taxable_amount = 0
        elif user_taxable_income >= data_bracket["max"]:
            taxable_amount = data_bracket["max"] - data_bracket["min"]
        else:
            taxable_amount = user_taxable_income - data_bracket["min"]
        
        tax_for_bracket = taxable_amount * data_bracket["rate"]
        total_tax += tax_for_bracket
    
    return total_tax           
            
def main():
    print("The United States Taxable Income for the year 2009")
    print("-----------------------------------------------------")
    print("\nFiling Status Options:")
    print("0 = Single filer")
    print("1 = Married filing jointly or qualified widow(er)")
    print("2 = Married filing separately")
    print("3 = Head of household")
    print()
    

    tax_data = load_tax_brackets()
    if tax_data is None:
        print("No file was found")
        return
    
    status = get_user_filing_status()
    print(f"Filing status {status} has been recorded.")
    print("-----------------------------------------------------")

    bracket = get_tax_bracket(status, tax_data)

    income = get_user_taxable_income()
    print(f"Taxable income {income} has been recorded")
    print("-----------------------------------------------------")

    tax_calculation = calculate_tax(bracket, income)
    print(f"Your total tax for the year 2009 is: ${tax_calculation:,.2f}")

main()



   
           
    

   
    
       






    



