from database.database import get_sum_of_current_field, get_duplicates_of_current_field, get_data, \
    get_sums_of_current_field_by_grouping, get_filter_data


def get_income() -> float:
    current_field = "figure"
    return get_sum_of_current_field(current_field)

def get_unpaid_invoices() -> float:
    current_field = "figure"
    condition = ("is_paid", 0)
    return get_sum_of_current_field(current_field, condition=condition)

def get_duplicate_invoices() -> list:
    current_field = "invoice_number"
    duplicates_data = get_duplicates_of_current_field(current_field)

    if duplicates_data:
        data = get_data()
        result = []
        result_separator = ('', '', '', '', '', '', '', '')

        for duplicate in duplicates_data:
            needed_number = duplicate[0]
            for invoice in data:
                invoice_number = invoice[2]
                if invoice_number == needed_number:
                    result.append(invoice)
            result.append(result_separator)
        return result[:-1]
    return []

def get_incomes_by_categories() -> list:
    current_field = "figure"
    grouping_field = "category"
    data = get_sums_of_current_field_by_grouping(current_field, grouping_field=grouping_field)

    if data:
        categories = []
        incomes = []

        for record in data:
            categories.append(record[0])
            incomes.append(record[1])
        return [categories, incomes]
    return [[], []]

def get_percent_of_paid_and_unpaid_invoices() -> list:
    all_invoices_count = len(get_data())
    if not all_invoices_count:
        return [[], []]

    attribute = "Платено"
    requirement = "Да"
    all_paid_invoices_count = len(get_filter_data(attribute, requirement))

    all_paid_invoices_percentage = round((all_paid_invoices_count / all_invoices_count) * 100, 2)
    all_unpaid_invoices_percentage = 100 - all_paid_invoices_percentage
    return [all_paid_invoices_percentage, all_unpaid_invoices_percentage]

def get_income_by_months() -> list:
    current_field = "figure"
    grouping_field = "strftime('%Y-%m', date)"
    data = get_sums_of_current_field_by_grouping(current_field, grouping_field=grouping_field)
    month_names = {'01': 'Януари', '02': 'Февруари', '03': 'Март', '04': 'Април',
                   '05': 'Май', '06': 'Юни', '07': 'Юли', '08': 'Август',
                   '09': 'Септември', '10': 'Октомври', '11': 'Ноември', '12': 'Декември'}

    if data:
        months = []
        incomes = []

        for record in data:
            year, month = record[0].split('-')
            months.append(f"{month_names[month]} {year}")
            incomes.append(record[1])
        return [months, incomes]
    return [[], []]
