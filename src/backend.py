import random
import pathlib
import csv
import item_exceptions
from view.gui import root

def main():
    '''Main routine'''
    # rand_list_1 = rand_list(rand_start=1, rand_end=10, rand_range=5)

    items_dir = file_dir(file_name='items.csv')
    read_items(file=items_dir)

    update_item(file=items_dir, name='sushi', price=6.5, quantity=15)
    create_item(file=items_dir, name='beer', price=2, quantity=10)

    read_items(file=items_dir)
    delete_item(file=items_dir, name='beer')
    read_item(file=items_dir, name='pizza box')

    
def rand_list(rand_start, rand_end, rand_range):

    rand_list = [random.randint(rand_start, rand_end) for _ in range(rand_range)]

    return [i for i in enumerate(rand_list)]

def file_dir(file_name):

    script_dir = pathlib.Path(__file__).parent

    rel_path = f'../files/{file_name}'

    return (script_dir / rel_path).resolve()

def create_item(file, name, price, quantity):
    # Used multiple context managers as 'a+' argument breaks the exception
    with file.open('a', newline='') as append_csv, file.open('r') as read_csv:
        # exception
        csv_reader = csv.DictReader(read_csv)

        for row in csv_reader:
            if name in row.values():
                raise item_exceptions.ItemAlreadyStored(
                    f'Can\'t create "{name}" as it already exists'
                )

        # append
        fieldnames = ['name', 'price', 'quantity']

        csv_writer = csv.DictWriter(append_csv, fieldnames=fieldnames)

        csv_writer.writerow({'name': name, 'price': price, 'quantity': quantity})

def read_item(file, name):

    with file.open('r', newline='') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        for row in csv_reader:
            if name in row.values():
                return row
            
        raise item_exceptions.ItemNotStored(
            f'Can\'t find "{name}" because it\'s not stored')

def read_items(file):

    with file.open(newline='') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        return [row for row in csv_reader]

# read and overwrite file
def update_item(file, name, price, quantity):

    with file.open('r+', newline='') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        csv_dicts = [row for row in csv_reader]

        item_names = [list(row.values())[0] for row in csv_dicts]

        # exception
        if name not in item_names:
            raise item_exceptions.ItemNotStored(
                f'Can\'t find "{name}" because it\'s not stored')

        # modify list while iterating
        csv_dicts[:] = [(row_dict if name not in row_dict.values()
                        else {'name' : name, 'price': price, 'quantity': quantity}) 
                        for row_dict in csv_dicts]

        csv_file.seek(0) # back to begining of the file.
        fieldnames = ['name', 'price', 'quantity']

        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        csv_writer.writeheader()
        for row in csv_dicts:
            csv_writer.writerow(row)

# read and overwrite file
def delete_item(file, name):

    with file.open('r+', newline='') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        csv_dicts = [row for row in csv_reader]

        item_names = [list(row.values())[0] for row in csv_dicts]

        # exception
        if name not in item_names:
            raise item_exceptions.ItemNotStored(
                f'Can\'t find "{name}" because it\'s not stored')

        # modify list while iterating
        csv_dicts[:] = [row_dict for row_dict in csv_dicts if name not in row_dict.values()]

        csv_file.seek(0) # back to begining of the file.
        csv_file.truncate() # truncate file to bring it to zero length.
        fieldnames = ['name', 'price', 'quantity']

        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        csv_writer.writeheader()
        for row in csv_dicts:
            csv_writer.writerow(row)

    
# Create a function that handles all exceptions (may increase project complexity eg. dependency)
# def already_stored(msg):
#     pass



if __name__ == '__main__':
    main()
    # root.mainloop()