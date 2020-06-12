from flask import jsonify
import datetime
from bson import ObjectId


class FoundVulsScan:
    def __init__(self, Method, URL, Affect, Data, Headers, Fingerprint):
        self.method = Method
        self.url = URL
        self.affect = Affect
        self.data = Data
        self.headers = Headers
        self.fingerprint = Fingerprint

    @property
    def convert_to_dict(self):
        to_dict = {}
        to_dict.update(self.__dict__)
        return to_dict


class FoundVulsVul:
    def __init__(self, VulXML, Severity, VulURL, From):
        self.xml_name = VulXML
        self.severity = Severity
        self.vul_vul = VulURL
        # from 是python关键字 暂时用from
        self.From = From

    @property
    def convert_to_dict(self):
        to_dict = {}
        to_dict.update(self.__dict__)
        to_dict['from'] = to_dict.pop('From')
        return to_dict


# // FoundVulDoc 检测到的漏洞结果，对应 CollectionFoundVuls
class FoundVulDoc:
    def __init__(self, Host, Scan, Vul, Context, AssetID):
        self.id = str(ObjectId())
        self.host = Host
        self.scan = Scan
        self.vul = Vul
        self.context = Context
        self.found_at = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        self.asset_id = AssetID

    @property
    def convert_to_dict(self):
        to_dict = {}
        to_dict.update(self.__dict__)
        return to_dict


