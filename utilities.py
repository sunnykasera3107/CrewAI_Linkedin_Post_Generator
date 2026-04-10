def convert_json_txt(json_content): #json in key: value form will be converted to simple text.
    if json_content != None and len(json_content) > 0:
        content = []
        for key, value in json_content.items():
            if type(value) in [list, dict]:
                value = convert_json_txt(value)
            content.append(f"{key}: {value}")
        return " ".join(content)
    return " "