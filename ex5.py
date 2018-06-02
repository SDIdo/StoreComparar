#####################################################
# FILE: EX5.py
# WRITERS: Ido Natan, Tom Poyarkov
# EXERCISE: EX5 intro2cs2
# DESCRIPTION: a program that compares between stores
######################################################

import xml.etree.ElementTree as ET

A_BIG_NUMBER = 999999
A_SMALL_NUMBER = -1
ZERO = 0
ONE = 1
PENALTY_PERCENTAGE = 1.25
RIGHT_BRACKET = '}'
LEFT_BRACKET = '{'
RG_SQ_BR = ']'
LF_SQ_BR = '['
EMPTY_SPACE = ''
TAB = '\t'
NEW_LINE = '\n'


def get_attribute(store_db, ItemCode, tag):
    '''
    Returns the attribute (tag) 
    of an Item with code: Itemcode in the given store
    :param store_db: a data structure of a store 
    :param ItemCode: a code of one of the items from the store
    :param_tag: one of the item properties
    '''
    return store_db[ItemCode][tag]


def string_item(item):
    '''
    Textual representation of an item in a store.
    Returns a string in the format of '[ItemCode] (ItemName)'
    :param item: an item from the store presented as a dictionary

    '''
    ret_str_p1 = LF_SQ_BR+item['ItemCode']+RG_SQ_BR
    ret_str_p2 = LEFT_BRACKET+item['ItemName']+RIGHT_BRACKET
    return ret_str_p1+TAB+ret_str_p2


def string_store_items(store_db):
    '''
    Textual representation of a store.
    Returns a string in the format of:
    string representation of item1
    string representation of item2
    :param store_db: a data structure of a store
    '''
    textual_store_representation = EMPTY_SPACE
    for key in store_db:
        item = store_db[key]
        textual_store_representation += string_item(item)+NEW_LINE

    return textual_store_representation


def read_prices_file(filename):
    '''
    Read a file of item prices into a dictionary.  The file is assumed to
    be in the standard XML format of "misrad haclcala".
    Returns a tuple: store_id and a store_db,
    where the first variable is the store name
    and the second is a dictionary describing the store. 
    The keys in this db will be ItemCodes of the different items and the
    values smaller  dictionaries mapping attribute names to their values.
    Important attributes include 'ItemCode', 'ItemName', and 'ItemPrice'
    :param filename: an xml file representing a store and it's items 
    '''
    tree = ET.parse(filename) 
    root = tree.getroot()
    stored_items = dict()
    store_id = root.find('StoreId').text
    """insertion of different item's elements to a dictionary,
    for every different ItemCode.
    Their tags as keys, actual names and values as values"""
    for item_traits in root.getiterator('Item'):
        item_props = dict()
        item_code = item_traits.find('ItemCode')
        for trait in item_traits:
            item_props[trait.tag] = trait.text
            """a dictionary of dictionaries, an arbitrary ItemCode as key to
            "it's" pack of elements, which were inserted in item_props
            dictionary, as value"""
        stored_items[item_code.text] = item_props
    return(store_id, stored_items)


def filter_store(store_db, filter_txt):  
    '''
    Create a new dictionary that includes only the items 
    that were filtered by user.
    I.e. items that text given by the user is part of their ItemName. 
    Args:
    :param store_db: a dictionary of dictionaries as created in 
     read_prices_file.
    :param filter_txt: the filter text as given by the user.
    returns a store after the filtering
    '''
    filtered_store = {}
    for item in store_db:
        if filter_txt in store_db[str(item)]['ItemName']:
            filtered_store[str(item)] = store_db[str(item)]
    return filtered_store


def create_basket_from_txt(basket_txt): 
    '''
    Receives text representation of few items (and maybe some garbage 
      at the edges)
    Returns a basket- list of ItemCodes that were included in basket_txt
    :param basket_txt: a text presentation of selected items (could also
    contain garbage as mentioned above)

    '''
    write_to_temp = False
    basket = []
    temp = EMPTY_SPACE
    for i in range(len(basket_txt)):
        if basket_txt[i] == LF_SQ_BR:
            if write_to_temp is True:
                temp = EMPTY_SPACE
            else:
                write_to_temp = True
            continue
        if basket_txt[i] == RG_SQ_BR and temp != EMPTY_SPACE:
            basket.append(str(temp))
            temp = EMPTY_SPACE
            write_to_temp = False
            if basket is not []:
                continue
        if write_to_temp is True:
            temp += basket_txt[i]
    return basket


def get_basket_prices(store_db, basket):
    '''
    Arguments: a store - dictionary of dictionaries and a basket - 
       a list of ItemCodes
    Go over all the items in the basket and create a new list 
      that describes the prices of store items
    In case one of the items is not part of the store, 
      its price will be None.
    '''

    basket_prices = []
    for ItemCodes in basket:
        if str(ItemCodes) in store_db:
            basket_prices.append(float(store_db[ItemCodes]['ItemPrice']))
        else:
            basket_prices.append(None)
    return basket_prices


def sum_basket(price_list):
    '''
    Receives a list of prices
    Returns a tuple - the sum of the list (when ignoring Nones) 
      and the number of missing items (Number of Nones)

    '''
    sum_price_list = ZERO
    missing_items = ZERO
    for i in range(len(price_list)):
        if price_list[i] != None:
            sum_price_list += price_list[i]
        else:
            missing_items += ONE
    return(sum_price_list, missing_items)

 
def basket_item_name(stores_db_list, ItemCode): 
    ''' 
    stores_db_list is a list of stores (list of dictionaries of 
      dictionaries)
    Find the first store in the list that contains the item and return its
    string representation (as in string_item())
    If the item is not avaiable in any of the stores return only [ItemCode]

    '''
    for i in range(len(stores_db_list)):
        if ItemCode in stores_db_list[i]:
            item_code = stores_db_list[i][ItemCode]['ItemCode']
            item_name = stores_db_list[i][ItemCode]['ItemName']
            ret_str_p1 = LF_SQ_BR + item_code + RG_SQ_BR
            ret_str_p2 = LEFT_BRACKET + item_name + RIGHT_BRACKET
            return ret_str_p1 + TAB + ret_str_p2
    return (LF_SQ_BR+ItemCode+RG_SQ_BR)


def save_basket(basket, filename):
    ''' 
    Save the basket into a file
    The basket reresentation in the file will be in the following format:
    [ItemCode1] 
    [ItemCode2] 
    ...
    [ItemCodeN]
    :param basket: a list consisting the selected items
    :param filename: a file destination to save the selected items at
    This function doesn't return anything.
    '''
    with open(filename, 'w') as opened_file:
        for itemCode in basket:
            opened_file.write(LF_SQ_BR+str(itemCode)+RG_SQ_BR)
            opened_file.write(NEW_LINE)


def load_basket(filename):
    ''' 
    Create basket (list of ItemCodes) from the given file.
    The file is assumed to be in the format of:
    [ItemCode1] 
    [ItemCode2] 
    ...
    [ItemCodeN]
    :param filename: a file destination to load the selected items from
    returns a list named 'basket' made of the items data from the file 
    '''
    basket = []
    with open(filename, 'r') as opened_file:
        item_codes = opened_file.readlines()
        for item_code in item_codes:
            new_item = item_code[1:len(item_code)-2]
            basket.append(new_item)
    return basket

def best_basket(list_of_price_list):
    '''
    Arg: list of lists, where each inner list is list of prices as created
    by get_basket_prices.
    Returns the cheapest store (index of the cheapest list) given that a 
    missing item has a price of its maximal price in the other stores *1.25
    :param list_of_price_list: list of lists that contains prices from the
    stores

    ''' 
    l = list_of_price_list
    mx = A_SMALL_NUMBER
    sm = ZERO
    is_best_sm = A_BIG_NUMBER
    for j in range(len(l)):
        sm = ZERO
        for i in range(len(l[j])):
            if l[j][i] != None:
                sm += l[j][i]
            else:
                mx = A_SMALL_NUMBER
                for q in range(len(l)):
                    if l[q][i] == None:
                        continue
                    elif mx < l[q][i]:
                        mx = l[q][i]
                sm += PENALTY_PERCENTAGE*mx
        if sm <= is_best_sm:
            is_best_sm = sm
            best_store_index = j
    return best_store_index