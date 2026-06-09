import re
import sqlite3
from datetime import datetime


DATABASE_FIELDS = {
        'ИД': 'id',
        'Дата': 'date',
        'Номер на фактура': 'invoice_number',
        'Клиент': 'client',
        'Сума': 'figure',
        'ДДС': 'tax',
        'Категория': 'category',
        'Платено': 'is_paid'
}
DATABASE_FILENAME = 'test.db'
TABLE_NAME = 'test'

INVOICE_NUMBER_REGEX = r"\bINV-\d{4,}\b"
DATE_REGEX = r"\b\d{2}/\d{2}/\d{4}\b"

def get_column_names() -> tuple:
    column_names = tuple(DATABASE_FIELDS.keys())
    return column_names

def create_database_and_table() -> None:
    query = f"CREATE TABLE IF NOT EXISTS {TABLE_NAME}(\
    id INTEGER PRIMARY KEY AUTOINCREMENT,\
    date VARCHAR(15) NOT NULL,\
    invoice_number VARCHAR(10) NOT NULL,\
    client VARCHAR(50) NOT NULL,\
    figure FLOAT NOT NULL,\
    tax FLOAT,\
    category VARCHAR(50) NOT NULL,\
    is_paid BOOLEAN DEFAULT FALSE\
    )"
    execute_query(query)

def get_data() -> list:
    query = f"SELECT * FROM {TABLE_NAME}"
    return execute_query(query)

def get_filter_data(attribute: str, requirement: str) -> list:
    current_field = DATABASE_FIELDS[attribute]
    requirement = validate_requirement(current_field, requirement)
    query = f"SELECT * FROM {TABLE_NAME} WHERE {current_field} = '{requirement}'"
    return execute_query(query)

def get_sum_of_current_field(current_field: str, condition=None) -> float:
    query = f"SELECT SUM({current_field}) FROM {TABLE_NAME}"
    if condition:
        needed_field = condition[0]
        value = condition[1]
        query += f" WHERE {needed_field} = '{value}'"
    result = execute_query(query)
    if result:
        return result[0][0]
    return 0

def get_sums_of_current_field_by_grouping(current_field: str, grouping_field: str) -> list:
    query = f"SELECT {grouping_field}, SUM({current_field}) FROM {TABLE_NAME} GROUP BY {grouping_field}\
            ORDER BY {grouping_field}"
    return execute_query(query)

def get_duplicates_of_current_field(current_field: str) -> list:
    query = f"SELECT {current_field}, COUNT(id) FROM {TABLE_NAME} GROUP BY {current_field}\
             HAVING COUNT(id) > 1 ORDER BY {current_field}"
    return execute_query(query)

def insert_data(data: list) -> None:
    fields = ", ".join(tuple(DATABASE_FIELDS.values())[1:])
    query = f"INSERT INTO {TABLE_NAME}({fields})\
            VALUES('{data[0]}','{data[1]}','{data[2]}',{data[3]},{data[4]},'{data[5]}',{data[6]})"
    execute_query(query)

def edit_data(attribute: str, requirement: str, second_attribute: str, value: str) -> str|None:
    needed_field = DATABASE_FIELDS[attribute]
    changing_field = DATABASE_FIELDS[second_attribute]
    requirement = validate_requirement(needed_field, requirement)
    value = validate_value(changing_field, value)
    if not value:
        return "Невалидни данни"
    query = f"UPDATE {TABLE_NAME} SET {changing_field} = '{value}' WHERE {needed_field} = '{requirement}'"
    execute_query(query)
    return None

def delete_data(attribute: str, requirement: str) -> None:
    current_field = DATABASE_FIELDS[attribute]
    requirement = validate_requirement(current_field, requirement)
    query = f"DELETE FROM {TABLE_NAME} WHERE {current_field} = '{requirement}'"
    execute_query(query)

def execute_query(query:str) -> list|None:
    conn = sqlite3.connect(DATABASE_FILENAME)
    cursor_obj = conn.cursor()
    cursor_obj.execute(query)
    data = None
    if query.startswith('SELECT'):
        data = cursor_obj.fetchall()
    conn.commit()
    conn.close()
    return data

def validate_requirement(current_field: str, requirement: str) -> int|str:
    if current_field == 'is_paid':
        requirement = requirement.lower()
        if requirement == 'да':
            return 1
        if requirement == 'не':
            return 0
        return ''
    return requirement

def validate_value(changing_field: str, value: str) -> str|float:
    if changing_field == 'is_paid':
        return validate_requirement(changing_field, value)
    if changing_field == 'invoice_number':
        if re.fullmatch(INVOICE_NUMBER_REGEX, value) is None:
            return ''
        return value
    if changing_field == 'figure' or changing_field == 'tax':
        try:
            value = float(value)
            if value <= 0:
                return ''
            return value
        except ValueError:
            return ''
    if changing_field == 'date':
        if re.fullmatch(DATE_REGEX, value) is None:
            return ''
        day, month, year = value.split('/')
        date = f"{year}-{month}-{day}"
        try:
            datetime.strptime(date, "%Y-%m-%d")
            return date
        except ValueError:
            return ''
    return value

def make_record_readable(record: list) -> list:
    record[0] = str(record[0])

    year, month, day = record[1].split('-')
    record[1] = f"{day}/{month}/{year}"

    record[4] = round(record[4], 2)
    record[5] = round(record[5], 2)

    if record[7]:
        record[7] = 'Да'
    else:
        record[7] = 'Не'

    return record
