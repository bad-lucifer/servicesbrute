## servicesbrute

### 描述

servicesbrute 基于nmap + masscan + hydra，以及flask + celery + redis+kafka框架， 

实现端口扫描 + 服务识别 + 服务弱口令探测 + 结果输出（kafka），实现面向服务弱口令的一条龙检测。

### 环境

python 3.6.4 / docker

### 使用

1. kafka配置  config.ini

2. celery配置 celeryConfig.py

3. docker-compose up

### 接口文档

#### 请求地址

开发：http://127.0.0.1:8082/servicebrute

**Method：** POST

**接口描述：** 执行服务弱口令检测模块

### 请求参数

**Form**

| 参数名称  |  是否必须 | 示例  | 备注  |

| ------------ | ------------ | ------------ | ------------ | 

| host | 是  |  127.0.0.1 | 目标IP或域名 |

| port | 是  |  4506 | 目标端口 |

| asset_id | 是  |  9192651770 | 资产ID |

| is_https | 是  |  Flase | 是否是https |

#### 响应说明

返回值只是反馈任务是否下发到异步执行 异步任务的执行结果会直接回传到kafka

```
{"code":1,"error":"","message":"already get task"}

code 1为成功 0为失败
error       报错信息
message     返回信息
```

