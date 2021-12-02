import circuit
import request
import time

if __name__ == "__main__":
    # Creating circuit with predefined parameters
    request_id = circuit.create_ochnc_wson_circuit("my_api_circuit", "RDM01", "PLINE-14-10", "RDM02", "PLINE-10-10")
    # Once created, check the status
    is_circuit_provisioning = True
    retry = 0
    while is_circuit_provisioning:
        time.sleep(2)
        completion_status = request.get_provisioning_request_status(request_id)
        print(f"Circuit completion status: {completion_status}")
        is_circuit_provisioning = not (completion_status == "SUCCESS")
        retry += 1
        if retry == 5:
            raise Exception("Circuit provisioning operation did not reach status SUCCESS")
    print("Circuit provisioned")
