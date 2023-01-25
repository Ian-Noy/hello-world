import yaml
import os
import collections
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


def update_file(service, changes, values_file):
    """
    This method updates changes in application chart values file
    :param: None
    :return: None
    """
    values_file_data = YAML().load(open(values_file))
    update_value = values_file_data
    for key in update_value[service]:
        try:
            update_value[service][key] = changes[key]
        except Exception as e:
            print(key + " - ", e)
    with open(values_file, 'w') as fp:
        YAML().dump(values_file_data, fp)


def get_values_from_file(service, file):
    """
    This method will return the requested service image and tag values
    :param service: Service to lookup
    :param file: File to look for specified key
    :return: Value
    """
    file_data = read_yaml_file(file)
    return file_data.get(service)


if __name__ == "__main__":
    services = ["service-one", "service-two"]
    config_file = os.getenv('CONFIG_FILE', 'pipeline/config.yaml')
    #environment = os.getenv('ENVIRONMENT')
    environment = "kraken"
    print(f"config_file: {config_file}, environment: {environment}, services: {services}")
    config = read_yaml_file(config_file)
    if config is None:
        print("Config file is empty")
        exit()

    for service in services:
        key = service + "-" + environment
        lt_key = service + "-loadtesting"
        charts_info = config.get(key)
        lt_charts_info = config.get(lt_key)
        if charts_info is None or charts_info == "" or lt_charts_info is None or lt_charts_info == "":
            print("chartsInfo does not exist in config file")
            exit()
        chart_root = charts_info.get("chartRoot")
        lt_chart_root = lt_charts_info.get("chartRoot")
        if chart_root is None or chart_root == "" or lt_charts_info is None or lt_charts_info == "":
            print("chartRoot value does not exist in chartsInfo")
            exit()
        service_file_name = charts_info.get("file")
        lt_service_file_name = lt_charts_info.get("file")
        if service_file_name is None or service_file_name == "" or lt_service_file_name is None or lt_service_file_name == "":
            print("valuesFile value does not exist in chartsInfo")
            exit()
        service_file = chart_root + "/" + service_file_name
        lt_service_file_name = lt_chart_root + "/" + lt_service_file_name
        service_values = get_values_from_file(service, service_file)
        if service_values is None or service_values == "":
            print("serviceValues not populated")
            exit()
        update_file(service, service_values, lt_service_file_name)
        
        
        
