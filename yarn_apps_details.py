import requests
import json
import sys
# usage  : python3 yarn_apps_details.py hdp-003
# purpose: 统计yarn 所有任务数在集群节点的分布情况
# 如果hostname 为ip地址，会从/etc/hosts映射中根据ip替换为hostname，故需要在hdp上执行该脚本
# 最简单的统计方法是将app_list中的所有信息存入数据库中,即可做简单的平台分析

def get_apps_hosts_distribution(apps_list):
    host_dict = {}
    for app in apps_list:
        host_name = app.get("host").strip()
        if not host_name:
            print("hostname not found in application details:", app)
            continue
        if host_name in host_dict.keys():
            host_dict[host_name] += 1
        else:
            host_dict[host_name] = 1

    return host_dict


# def get_apps_details(apps_list):
#     pass


def get_hostname_map():
    with open('/etc/hosts', 'r') as f:
        host_file = f.readlines()
    ip_host_dict = {}
    for line in host_file:
        ip_host_list = line.strip().split(" ")
        if len(ip_host_list) == 2:
            ip_host_dict[ip_host_list[0]] = ip_host_list[1]
        else:
            continue
    return ip_host_dict


if __name__ == '__main__':

    timeline_v1_server = sys.argv[1]
    resp = requests.get("http://{}:8188/ws/v1/applicationhistory/apps".format(timeline_v1_server))

    json_obj = json.loads(resp.text)

    apps_list = json_obj.get("app") if json_obj else None
    ip_hostname_dict = get_hostname_map()
    hosts_dict = get_apps_hosts_distribution(apps_list)
    host_list = list(hosts_dict.keys())

    for hostname in host_list:
        if hostname in ip_hostname_dict.keys():
            if ip_hostname_dict[hostname] in host_list:
                hosts_dict[ip_hostname_dict[hostname]] += hosts_dict[hostname]
            else:
                hosts_dict[ip_hostname_dict[hostname]] = hosts_dict[hostname]

            del hosts_dict[hostname]
        else:
            # print("skip key: ", hostname)
            continue
    print("任务总数为:", len(apps_list), "统计到的任务数量为：", sum(hosts_dict.values()))
    print(hosts_dict)

