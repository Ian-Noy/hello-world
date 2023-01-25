import yaml
import os
import json
from ruamel.yaml import YAML

def read_yaml_file(file):
    """
    This method reads the yaml config file from the specified location
    :param file: Path to configuration file to be processed
    :return: file content
    """
    try:
        with open(file, 'r') as stream:
            return yaml.safe_load(stream)
    except FileNotFoundError:
        print(f"'{file}' file not found")
        exit()


def update_file():
    """
    This method updates changes in application chart values file
    :param: None
    :return: None
    """
    change_list = json.loads(changes)
    print("Changes to be updated - ", change_list)
    values_file_data = YAML().load(open(values_file))
    for change in change_list:
        value_path = change.get("jsonPath").split(".")
        update_value = values_file_data
        print(value_path)
        for path in value_path[:-1]:
            update_value = update_value.get(path)
        try:
            update_value[value_path[-1]] = change.get("value")
        except Exception as e:
            print(key + " - ", e)
    with open(values_file, 'w') as fp:
        YAML().dump(values_file_data, fp)

if __name__ == "__main__":
    services = ["service-one", "service-two"]
    config_file = os.getenv('CONFIG_FILE', 'pipeline/config.yaml')
    environment = os.getenv('ENVIRONMENT')
    print(f"config_file: {config_file}, environment: {environment}, services: {services}")
    config = read_yaml_file(config_file)
    if config is None:
        print("Config file is empty")
        exit()

    for service in services:
        key = service + "-" + environment
        charts_info = config.get(key)
        if charts_info is None or charts_info == "":
            print("chartsInfo does not exist in config file")
            exit()
        chart_root = charts_info.get("chartRoot")
        if chart_root is None or chart_root == "":
            print("chartRoot value does not exist in chartsInfo")
            exit()
        values_file_name = charts_info.get("file")
        if values_file_name is None or values_file_name == "":
            print("valuesFile value does not exist in chartsInfo")
            exit()
        values_file = chart_root + "/" + values_file_name
        print(f"Values_file: {values_file}")
