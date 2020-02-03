import requests


class Emias:
    @staticmethod
    def deparments(omsNumber: str, birthDate: str) -> list:
        """
        :param omsNumber: len(omsNumber) == 11 and omsNumber.isdigit() == True
        :param birthDate: YYYY-MM-DD
        :return: pass
        """

        url = "https://emias.info/api/new/eip2/?getSpecialitiesInfo"
        data = {
            "jsonrpc": "2.0",
            "id": "",
            "method": "getSpecialitiesInfo",
            "params": {"omsNumber": omsNumber, "birthDate": birthDate,},
        }

        response = requests.post(url, json=data)
        result = response.json()["result"]
        return result

    @staticmethod
    def doctors(omsNumber: str, birthDate: str, specialityId: str) -> list:
        """
        :param omsNumber: len(omsNumber) == 11 and omsNumber.isdigit() == True
        :param birthDate: YYYY-MM-DD
        :param specialityId:  specialityId.isdigit() == True
        :return: pass
        """

        url = "https://emias.info/api/new/eip2/?getDoctorsInfo"
        data = {
            "jsonrpc": "2.0",
            "id": "",
            "method": "getDoctorsInfo",
            "params": {
                "omsNumber": omsNumber,
                "birthDate": birthDate,
                "specialityId": specialityId,
            },
        }

        response = requests.post(url, json=data)
        result = response.json()["result"]
        return result

    @staticmethod
    def schedule(omsNumber: str, birthDate: str, availableResourceId: int) -> dict:
        """
        :param omsNumber: len(omsNumber) == 11 and omsNumber.isdigit() == True
        :param birthDate: YYYY-MM-DD
        :param availableResourceId: pass
        :return: pass
        """

        url = "https://emias.info/api/new/eip2/?getAvailableResourceScheduleInfo"
        data = {
            "jsonrpc": "2.0",
            "id": "",
            "method": "getAvailableResourceScheduleInfo",
            "params": {
                "omsNumber": omsNumber,
                "birthDate": birthDate,
                "availableResourceId": availableResourceId,
            },
        }

        response = requests.post(url, json=data)
        result = response.json()["result"]
        return result

    @staticmethod
    def create_appointment(
        omsNumber: str,
        birthDate: str,
        availableResourceId: int,
        complexResourceId: int,
        receptionTypeId: str,
        startTime: str,
        endTime: str,
    ) -> dict:
        """
        :param omsNumber: len(omsNumber) == 11 and omsNumber.isdigit() == True
        :param birthDate: YYYY-MM-DD
        :param availableResourceId: pass
        :param complexResourceId: pass
        :param receptionTypeId: receptionTypeId.isdigit() == True
        :param startTime: YYYY-MM-DDTHH:MM:SS+03:00
        :param endTime: YYYY-MM-DDTHH:MM:SS+03:00
        :return: pass
        """

        url = "https://emias.info/api/new/eip2/?createAppointment"
        data = {
            "jsonrpc": "2.0",
            "id": "",
            "method": "createAppointment",
            "params": {
                "omsNumber": omsNumber,
                "birthDate": birthDate,
                "availableResourceId": availableResourceId,
                "complexResourceId": complexResourceId,
                "receptionTypeId": complexResourceId,
                "startTime": startTime,
                "endTime": endTime,
            },
        }

        import json
        print(json.dumps(data))
        response = requests.post(url, json=data)
        result = response.json()["result"]
        return result
