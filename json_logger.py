import json
import date_time

file_path = ""

def write_command(user, command: str):
    default_dict = {
        "Date": date_time.persian_date("%Y/%m/%d"),
        "Time": date_time.tehran_datetime("%X"),
        "User": user,
        "Command": command
    }

    write_file(default_dict)

def write_text(user, report_dic: dict):
    default_dict = {
        "Date": date_time.persian_date("%Y/%m/%d"),
        "Time": date_time.tehran_datetime("%X"),
        "User": user,
    }
    for key, value in report_dic.items():
        default_dict[key] = value
    write_file(default_dict)

def write_file(json_dict: dict):
    with open(file=file_path, mode='a', encoding='utf-8') as file:
        json_text = json.dumps(json_dict, indent=4, ensure_ascii=False)
        json_text += ',\n'
        file.write(json_text)

def clear():
    open(file_path, 'w').close()
