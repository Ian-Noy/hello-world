import yaml
import os
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
    :param service: Name of service to update
    :param changes: Dict containing image and tag values to update
    :param values_file: Path to values file that will be updated
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


def find_service_file(service, environment):
    """
    This method will find the service file for a given environment
    :param service: Name of service
    :param environment: Environment to find
    :return: Path of the service file
    """
    key = service + "-" + environment
    charts_info = config.get(key)
    if charts_info is None or charts_info == "":
        raise ValueError("chartsInfo does not exist in config file")
    chart_root = charts_info.get("chartRoot")
    if chart_root is None or chart_root == "":
        raise ValueError("chartsInfo does not exist in config file")
    service_file_name = charts_info.get("file")
    if service_file_name is None or service_file_name == "":
        raise ValueError("valuesFile value does not exist in chartsInfo")
    
    return chart_root + "/" + service_file_name


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
        try:
            env_service_file = find_service_file(service, environment)
            lt_service_file = find_service_file(service, "loadtesting")
        except ValueError:
            raise

        service_values = read_yaml_file(env_service_file).get(service)
        if service_values is None or service_values == "":
            print("serviceValues not populated")
            exit()
        update_file(service, service_values, lt_service_file)
        
        
        
