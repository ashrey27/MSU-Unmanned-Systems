###############################################################################
#       
#                               TAX CALCULATOR
#   - Enter total taxes summed
#       - Calculates state and county taxes paid plus the original amount
#           - North Carolina state tax applied
#           - Orange county tax applied
#
###############################################################################

def e_585(tot_tax):
    state_tax = tot_tax * 0.67855 #total tax split into state and county
    county_tax = tot_tax * 0.32144
    print("state original: " + "{:.{}f}".format(state_tax, 2))
    print("county original: " + "{:.{}f}".format(county_tax, 2)) 
    tot_state = state_tax / 0.0725 #division by total North Carolina tax rate
    tot_county = county_tax / 0.0725
    print("state total: " + "{:.{}f}".format(tot_state, 2))
    print("county total: " + "{:.{}f}".format(tot_county, 2))
    return None

def main():
    insert = float(input("enter total taxes: "))
    result = e_585(insert)

if __name__ == "__main__":
    main()