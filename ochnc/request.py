import requests
import os


def get_provisioning_request_status(request_id):
    """
    Retrieves the status of a circuit provisioning request
    :param request_id: A side of the circuit (device
    :return: request completion status
    """
    # TODO: payload is too big. Should use jinja or be placed in another file

    url = f"https://{os.getenv('EPNM_ENDPOINT')}/restconf/operations/v1/cisco-service-activation:provision-service?request-id={request_id}"
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    response = requests.request("GET", url, headers=headers,
                                auth=(os.getenv('EPNM_USER'), os.getenv('EPNM_PASSWORD')),verify=False)
    response.raise_for_status()
    return response.json()["com.response-message"]["com.data"]["saext.provision-service-request"]["completion-status"]
