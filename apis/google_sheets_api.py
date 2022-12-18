from apis.snippets.sheet_append_values import append_values
from apis.snippets.sheet_get_values import get_values
from apis.snippets.sheet_update_values import update_values

SPREADSHEET_ID = '1woHLQaJU4PKlurYx2cT0k89pXVCRQBN0Hwr1rxgAUQI'

objects = {
    'library_card': {
        'sheet_name': 'TheThuVien',
        'start_col': 'A',
        'end_col': 'J',
        'id_col': 'A',
        'name_col': 'B',
        'delete_col': 'K',
        'delete_pos': 10,
        'start_row': 2,
        'end_row': 1000
    },
    'lend_slip': {
        'sheet_name': 'PhieuMuon',
        'start_col': 'A',
        'end_col': 'D',
        'id_col': 'A',
        'name_col': 'B',
        'delete_col': 'E',
        'delete_pos': 4,
        'start_row': 2,
        'end_row': 1000
    },
    'lend_slip_detail': {
        'sheet_name': 'ChiTietPhieuMuon',
        'start_col': 'A',
        'end_col': 'B',
        'id_col': 'A',
        'name_col': 'B',
        'delete_col': 'C',
        'delete_pos': 2,
        'start_row': 2,
        'end_row': 1000
    },
    'return_slip': {
        'sheet_name': 'PhieuTra',
        'start_col': 'A',
        'end_col': 'C',
        'id_col': 'A',
        'name_col': 'B',
        'delete_col': 'D',
        'delete_pos': 3,
        'start_row': 2,
        'end_row': 1000
    },
    'return_slip_detail': {
        'sheet_name': 'ChiTietPhieuTra',
        'start_col': 'A',
        'end_col': 'B',
        'id_col': 'A',
        'name_col': 'B',
        'delete_col': 'C',
        'delete_pos': 2,
        'start_row': 2,
        'end_row': 1000
    },
    'book': {
        'sheet_name': 'Sach',
        'start_col': 'A',
        'end_col': 'J',
        'id_col': 'A',
        'name_col': 'B',
        'delete_col': 'K',
        'delete_pos': 10,
        'start_row': 2,
        'end_row': 1000
    },
    'publisher': {
        'sheet_name': 'NhaXuatBan',
        'start_col': 'A',
        'end_col': 'D',
        'id_col': 'A',
        'name_col': 'B',
        'delete_col': 'E',
        'delete_pos': 4,
        'start_row': 2,
        'end_row': 1000
    },
    'author': {
        'sheet_name': 'TacGia',
        'start_col': 'A',
        'end_col': 'B',
        'id_col': 'A',
        'name_col': 'B',
        'delete_col': 'C',
        'delete_pos': 2,
        'start_row': 2,
        'end_row': 1000
    },
    'category': {
        'sheet_name': 'TheLoaiSach',
        'start_col': 'A',
        'end_col': 'B',
        'id_col': 'A',
        'name_col': 'B',
        'delete_col': 'C',
        'delete_pos': 2,
        'start_row': 2,
        'end_row': 1000
    },
    'position': {
        'sheet_name': 'ViTri',
        'start_col': 'A',
        'end_col': 'B',
        'id_col': 'A',
        'name_col': 'B',
        'delete_col': 'C',
        'delete_pos': 2,
        'start_row': 2,
        'end_row': 1000
    }
}

def range_name(sheet_name, start_col, start_row, end_col, end_row):
    return f'{sheet_name}!{start_col}{start_row}:{end_col}{end_row}'

def parse_object_name(object_name):
    result = objects[object_name]
    if (result): return result
    else: return None

def get_all_list(object):
    value_range = get_values(
        SPREADSHEET_ID,
        range_name(object['sheet_name'], object['start_col'], object['start_row'], object['delete_col'], object['end_row'])
    )
    result = value_range.get('values', [])
    return result

def get_value_list(object):
    value_range = get_values(
        SPREADSHEET_ID,
        range_name(object['sheet_name'], object['start_col'], object['start_row'], object['end_col'], object['end_row'])
    )
    result = value_range.get('values', [])
    return result

def get_id_list(object):
    id_range = get_values(
        SPREADSHEET_ID,
        range_name(object['sheet_name'], object['id_col'], object['start_row'], object['id_col'], object['end_row'])
    )
    result = id_range.get('values', [])
    return result

def get_name_list(object):
    name_range = get_values(
        SPREADSHEET_ID,
        range_name(object['sheet_name'], object['name_col'], object['start_row'], object['name_col'], object['end_row'])
    )
    result = name_range.get('values', [])
    return result

def get_delete_list(object):
    delete_range = get_values(
        SPREADSHEET_ID,
        range_name(object['sheet_name'], object['delete_col'], object['start_row'], object['delete_col'], object['end_row'])
    )
    result = delete_range.get('values', [])
    return result

def find_element_by(object, field_type, field, found = False, pos = 0):
    # Check
    if (not field_type or not field):
        print('Null field_type or field!')
        return [found, pos]

    delete_list = get_delete_list(object)
    match field_type:
        case 'id':
            id_list = get_id_list(object)
            while (pos < len(id_list)):
                if (field == id_list[pos][0] and delete_list[pos][0] != '1'):
                    found = True
                    break
                pos += 1
        case 'name':
            name_list = get_name_list(object)
            while (pos < len(name_list)):
                if (field == name_list[pos][0] and delete_list[pos][0] != '1'):
                    found = True
                    break
                pos += 1
    result = [found, pos]
    return result

def filter_element_list_by(object, field_type, field):
    # Check
    if (not field_type or not field):
        print('Null field_type or field!')
        return []

    delete_list = get_delete_list(object)
    pos_arr = []
    result = []
    match field_type:
        case 'id':
            id_list = get_id_list(object)
            p = 0
            while (p < len(id_list)):
                if (field == id_list[p][0] and delete_list[p][0] != '1'):
                    pos_arr.append(p)
                p += 1
            value_list = get_value_list(object)
            for pos in pos_arr:
                result.append(value_list[pos])
        case 'name':
            name_list = get_name_list(object)
            p = 0
            while (p < len(name_list)):
                if (str(name_list[p][0]).find(field) != -1 and delete_list[p][0] != '1'):
                    pos_arr.append(p)
                p += 1
            value_list = get_value_list(object)
            for pos in pos_arr:
                result.append(value_list[pos])
    return result

def append_element(object_name, values, allow_duplicate_ids = False):
    # Check
    object = parse_object_name(object_name)
    if (object == None): return False
    if (not values):
        print('Null values!')
        return False

    if (not allow_duplicate_ids):
        find_result = find_element_by(object, 'id', values[0])
        if (find_result[0]):
            print('Id already exists!')
            return False
    
    values.append('0')

    value_range = append_values(
        SPREADSHEET_ID,
        range_name(object['sheet_name'], object['start_col'], object['start_row'], object['delete_col'], object['end_row']),
        [values]
    )
    result = value_range.get('updates', [])
    # print(result)
    return result

def get_element_list(object_name):
    # Check
    object = parse_object_name(object_name)
    if (object == None): return False

    result = []
    all_list = get_all_list(object)
    for pos in range(len(all_list)):
        # Check if IsDeleted
        row_deleted = all_list[pos][object['delete_pos']]
        if (row_deleted != '1'):
            value = list(all_list[pos])
            value.pop()
            result.append(value)
    # print(result)
    return result

def get_element_by_id(object_name, id):
    # Check
    object = parse_object_name(object_name)
    if (object == None): return False
    if (not id): return get_element_list(object_name)

    find_result = find_element_by(object, 'id', id)
    if (not find_result[0]):
        print('No id found.')
        return False

    pos = find_result[1]

    value_range = get_values(
        SPREADSHEET_ID,
        range_name(object['sheet_name'], object['start_col'], pos + 2, object['end_col'], pos + 2)
    )
    result = value_range.get('values', [])
    # print(result)
    return result

def get_element_list_by(object_name, field_type, field):
    # Check
    object = parse_object_name(object_name)
    if (object == None): return False
    if (not field): return get_element_list(object_name)

    result = filter_element_list_by(object, field_type, field)
    # print(result)
    return result

def update_element(object_name, values):
    # Check
    object = parse_object_name(object_name)
    if (object == None): return False
    if (not values):
        print('Null values!')
        return False

    find_result = find_element_by(object, 'id', values[0])
    if (not find_result[0]):
        print('No id found.')
        return False

    pos = find_result[1]

    value_range = update_values(
        SPREADSHEET_ID,
        range_name(object['sheet_name'], object['start_col'], pos + 2, object['end_col'], pos + 2),
        [values]
    )
    result = value_range
    # print(result)
    return result

def delete_element_by(object_name, field_type, field):
    # Check
    object = parse_object_name(object_name)
    if (object == None): return False
    if (not field_type or not field):
        print('Null field_type or field!')
        return False

    find_result = find_element_by(object, field_type, field)
    if (not find_result[0]):
        print('No id found.')
        return False

    pos = find_result[1]
    values = ['1']

    value_range = update_values(
        SPREADSHEET_ID,
        range_name(object['sheet_name'], object['delete_col'], pos + 2, object['delete_col'], pos + 2),
        [values]
    )
    result = value_range
    # print(result)
    return result

if __name__ == '__main__':
    object_name = 'lc'
    # print(get_objects(object_name))
    # get_object_by_id(object_name, '10')
    # get_objects_by_name(object_name, 'K')
    # append_object(object_name, ['12', 'test', '3', '5', '2', '100', '2000', '10', '10', '80000'])
    # update_object(object_name, ['9', 'test', '1', '1', '1', '100', '2000', '10', '10', '80000'])
    # delete_object_by_id(object_name, '5')
