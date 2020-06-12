#!/usr/bin/env python
# -*- coding: utf-8 -*-
from lib.hydra_plugin import nmapscan,service_check,hydra_scanner
from lib.send2kafka import send_to_kafka
from lib.tools import *
import configparser


def starter(host, port, asset_id, is_https):

    config = configparser.ConfigParser()
    config.read("config.ini", encoding="utf-8")

    support_service_list = config['services']['name']

    xml = 'weak_user_pass.xml'
    try:
        print(host)
        service_dict, real_ip = nmapscan(host)
        if service_dict:
            for port in service_dict.keys():
                service = service_dict[port]['name']
                # 检查该服务是否支持爆破
                if service in support_service_list:
                    check_result = service_check(real_ip, service, '')
                    if check_result:
                        result = hydra_scanner(real_ip, service, '')
                        for single_result in result:
                            scan = FoundVulsScan('', host, 'weak password', str(single_result), {}, 'weak password')
                            vul = FoundVulsVul(xml, 'high', host, '')
                            doc = FoundVulDoc(host, scan.convert_to_dict, vul.convert_to_dict, {}, asset_id)

                            print(doc.convert_to_dict)

                            # 输出结果
                            send_to_kafka(doc.convert_to_dict)
                else:
                    print(service + " not support brute")
    except Exception as e:
        print(e)



