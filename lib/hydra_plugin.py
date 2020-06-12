#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import signal
import shlex
import re
import nmap
from datetime import datetime
from subprocess import PIPE, Popen


class HydraScanner:

    def __init__(self, target, service, args):
        self.target = target
        self.service = service
        self.username_list_path = 'dict/user'
        self.password_list_path = 'dict/pwd'
        self.args = args
        self.stdout = ''
        self.stderr = ''
        self.result = []

    def scanner(self):
        if not os.path.exists(self.username_list_path):
            return 'username dict not exist'
        if not os.path.exists(self.password_list_path):
            return 'password dict not exist'
        command = self._format_args()
        process = Popen(command, stdout=PIPE, stderr=PIPE)
        try:
            (self.stdout, self.stderr) = process.communicate()
            self.stdout = self.stdout.decode("utf-8")
            # print self.stdout
        except Exception as e:
            print(process.pid, e)
        return self._format_res()

    def _format_args(self):
        if self.service in ['redis', 'cisco', 'oracle-listener', 's7-300', 'snmp', 'vnc']:
            # hydra -w 30 -p 123456 redis://192.168.1.1
            command = 'hydra -w 30 %s -P %s %s://%s' % (self.args, self.password_list_path, self.service, self.target)

        else:
            # hydra -w 30 -L user -P pwd mysql://192.168.1.1
            command = 'hydra -w 30 %s -L %s -P %s %s://%s' % (
            self.args, self.username_list_path, self.password_list_path,
            self.service, self.target)
        print(command)
        return shlex.split(command)

    def _format_res(self):
        result_list = []
        result = {}
        pattern_res = '(\[\d+\]\[%s\]\shost:\s\d+\.\d+\.\d+\.\d+.*?)\n' % self.service
        pattern_host = 'host:\s(\d+\.\d+\.\d+\.\d+)\s'
        pattern_username = 'login:\s(.+?)\s+password:'
        pattern_password = 'password:\s(.+?)$'
        re_result = re.findall(pattern_res, self.stdout)
        print(re_result)
        for res in re_result:
            try:
                if re.findall(pattern_host, res):
                    host = re.findall(pattern_host, res)[0]
                else:
                    host = 'None'
                if re.findall(pattern_username, res):
                    username = re.findall(pattern_username, res)[0]
                else:
                    username = "None"
                if re.findall(pattern_password, res):
                    password = re.findall(pattern_password, res)[0]
                else:
                    password = "None"
                result['target'] = host
                result['service'] = self.service
                result['username'] = username
                result['password'] = password
                result_list.append(result)
                result = {}
            except Exception as e:
                print(res, e)
        return result_list


class ServiceCheck:

    def __init__(self, target, service, args):
        self.target = target
        self.service = service
        self.args = args
        self.username = 'None'
        self.password = 'None'
        self.stdout = ''
        self.stderr = ''
        self.flag_list = [
            'Anonymous success',
            'not require password'
        ]

    def service_check(self):
        # print("[*] Service Check %s %s" % (self.target, self.service))
        command = self._format_args()
        print(command)
        start_time = datetime.now()
        process = Popen(command, stdout=PIPE, stderr=PIPE)
        try:
            while process.poll() is None:
                now_time = datetime.now()
                if (now_time - start_time).seconds > 15:
                    try:
                        os.kill(process.pid, signal.SIGTERM)
                    except OSError as e:
                        print(process.pid, e)
                    return False
            (self.stdout, self.stderr) = process.communicate()
            # byte to str
            self.stdout = self.stdout.decode("utf-8")
            self.stderr = self.stderr.decode("utf-8")

        except Exception as e:
            print(process.pid, e)
        return self.host_check()

    def _format_args(self):
        if self.service in ['redis', 'cisco', 'oracle-listener', 's7-300', 'snmp', 'vnc']:
            # hydra -w 30 -p 123456 redis://192.168.1.1
            command = 'hydra -w 30 %s -p %s %s://%s' % (self.args, self.password, self.service, self.target)

        else:
            # hydra -w 30 -l root -p 123456 mysql://192.168.1.1
            command = 'hydra -w 30 %s -l %s -p %s %s://%s' % (self.args, self.username, self.password,
                                                              self.service, self.target)
        return shlex.split(command)

    def host_check(self):
        # 如果碰巧check的时候就爆出了账号密码...直接返回
        for flag in self.flag_list:
            if flag in self.stderr:
                print(flag, self.stderr)
                return {"target": self.target, "result": {'username': self.username, "password": self.password}}
        if "successfully" in self.stdout and self.target in self.stdout:
            print(self.stderr)
            return {"target": self.target, "result": {'username': self.username, "password": self.password}}
        # 如果爆破 返回false
        elif 'ERROR' in self.stderr or 'waiting for children to finish' in self.stdout:
            return False
        # 协议支持爆破、且目标通的话 返回true
        else:
            return True


def hydra_scanner(target, service, args):
    start = HydraScanner(target, service, args)
    result = start.scanner()
    return result


def service_check(target, service, args):
    start = ServiceCheck(target, service, args)
    result = start.service_check()
    return result


"""
# 如果端口数量大于50，说明可能存在防火墙...
"""


def nmapscan(scan_ip):
    try:
        nms = nmap.PortScanner()
        # temp = nms.scan(scan_ip ,'0-65535','-sV')
        temp = nms.scan(scan_ip, None, '-sV --open --host-timeout 600')
        # 处理域名
        print(temp['scan'])
        if temp['scan']:
            scan_ip = list(temp['scan'])[0]
            scan_result = temp['scan'][scan_ip]['tcp']
            print(scan_result)
            if len(scan_result.keys()) > 50:
                scan_result = {}
            return scan_result, scan_ip
        else:
            print("nmap finish and found nothing")
            return {}, ""
    except Exception as e:
        print(e)