def read_file(file_str):
    fir_name = []
    sec_name = []
    
    while True:
        try:
            file_obj = open(file_str, 'r')
            print("Opened the file: ", file_str)
            break
        except IOError:
            print("File failed to open. Enter a valid file name")
            file_str = input("Enter me a file to open: ")

    file_obj.readline()
    for row in file_obj:
        for col in row.split():
            
            fir_name.append(row)
    
    file_obj.close()
    return fir_name

def main():
    open_file = str(input("enter file name: "))
    action = read_file(open_file)
    print(action)

if __name__ == "__main__":
    main()