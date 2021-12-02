import requests
import os


def create_ochnc_wson_circuit(service_name, device_a, interface_a, device_z, interface_z):
    """
    Creates a OCHNC WSON circuit
    :param device_a: A side of the circuit (device
    :param interface_a: Interface to be used from the A side device
    :param device_z: Z side of the circuit (device)
    :param interface_z: Interface to be used from the A side device
    :return: Request ID
    """
    # TODO: payload is too big. Should use jinja or be placed in another file
    request_payload = {
        "sa.service-order-data": {
            "sa.customer-ref": "MD=CISCO_EPNM!CUSTOMER=Infrastructure",
            "sa.service-name": service_name,
            "sa.service-description": "API created circuit",
            "sa.service-type": "optical",
            "sa.service-subtype": "OCHNC",
            "sa.service-activate": "true",
            "sa.direction": "BIDIRECTIONAL",
            "sa.optical-data": {
                "sa.uni": "false",
                "sa.label": "",
                "sa.protection": "NONE",
                "sa.ochnc-data": {
                    "sa.validation": "NONE",
                    "sa.restoration": "NONE",
                    "sa.priority": "LOW",
                    "sa.validation-restoration": "NONE"
                }
            },
            "sa.termination-point-list": {
                "sa.termination-point-config": [
                    {
                        "sa.tp-ref": f"MD=CISCO_EPNM!ND={device_a}!CTP=name={interface_a}-RX;lr=lr-optical-section",
                        "sa.directionality": "source",
                        "sa.optical-data": {
                            "sa.ochnc-data": {
                                "sa.drop-port-ref": f"MD=CISCO_EPNM!ND={device_a}!CTP=name={interface_a}-TX;lr=lr-optical-section"
                            }
                        }
                    },
                    {
                        "sa.tp-ref": f"MD=CISCO_EPNM!ND={device_z}!CTP=name={interface_z}-RX;lr=lr-optical-section",
                        "sa.directionality": "sink",
                        "sa.optical-data": {
                            "sa.ochnc-data": {
                                "sa.drop-port-ref": f"MD=CISCO_EPNM!ND={device_z}!CTP=name={interface_z}-TX;lr=lr-optical-section"
                            }
                        }
                    }
                ]
            }
        }
    }
    url = f"https://{os.getenv('EPNM_ENDPOINT')}/restconf/operations/v1/cisco-service-activation:provision-service"
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, json=request_payload,
                                auth=(os.getenv('EPNM_USER'), os.getenv('EPNM_PASSWORD')),verify=False)
    response.raise_for_status()
    return response.json()["sa.provision-service-response"]["sa.request-id"]
