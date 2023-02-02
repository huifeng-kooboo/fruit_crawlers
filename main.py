import requests
import json
import csv
from datetime import datetime

def get_time_str():
    return datetime.now().strftime('%Y_%m_%d')

'''
一级菜单名称 ☑️
二级菜单名称 ☑️
三级菜单名称 ☑️
详细商品名称 （goodsName） ☑️
商品ID（goodsId）☑️
商家（shopName）
剩余（inventory）
毛重（grossWeight）
净重（suttle）
单价（nowPrice）
成本价（=单价+毛重*0.3+2）
成本单价（空一列）
报价（=成本价/（1-0.3））
报价单价（空一列）
人物场（=报价*0.05）
利润（=报价-成本价-人物场）
利润率（=利润/报价）
产地（goodsAttribute）
货源（goodsAttribute）
等级（goodsAttribute）
商品说明（goodsInstruction）
售后情况（freeAfterSales）
封面图片（goodsCover）
商品图片（goodsImage）
视频地址（goodsVideo）
'''



g_headers = {
    'User-Agent':"Mozilla/5.0 (iPhone; CPU iPhone OS 11_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E217 MicroMessenger/6.8.0(0x16080000) NetType/WIFI Language/en Branch/Br_trunk MiniProgramEnv/Mac",
    'Content-Type':"application/x-www-form-urlencoded",
    'Referer':'https://servicewechat.com/wxa3fada743c1691ba/64/page-frame.html',
    'Host':'hb-api.degeguoyun.com',
    'Connection':'keep-alive',
    'Accept':'*/*',
    'Accept-Encoding':'gzip, deflate, br',
}

#####################################config###########################################
g_sort_url = 'https://hb-api.degeguoyun.com/api/sortInfo/tree?parentId=0'

g_fruit_url = 'https://hb-api.degeguoyun.com/api/goodsInfo/queryBySortId?sortId={0}&sortLevel={1}&pageSize=10&pageNum={2}&isAsc=desc&orderByColumn='

g_detail_url = 'https://hb-api.degeguoyun.com/api/goodsInfo/getGoodInfoByGoodsId?goodsId={0}&status=1'


def get_menu_info():
    """获取一级菜单目录
    """
    res = requests.get(g_sort_url,headers=g_headers)
    res.encoding = 'utf-8'
    json_data = json.loads(res.text)
    list_data = json_data['rows']
    for data in list_data:
        print(f"一级菜单名称:{data['sortName']},sortId:{data['id']},sortLevel:{data['sortLevel']}")
        if data.get("childrenList",None) != None:
            child_list = data.get("childrenList")
            for child in child_list:
                print(f"二级菜单名称: {child['sortName']},sortId:{child['id']},sortLevel:{child['sortLevel']}")
                if child.get("childrenList",None) != None:
                    third_child_list = child.get("childrenList")
                    for third_child in third_child_list:
                        print(f"三级菜单名称: {third_child['sortName']},sortId:{third_child['id']},sortLevel:{third_child['sortLevel']}")
                        fruit_url = g_fruit_url.format(third_child['id'], third_child['sortLevel'],1)
                        res_fruit = requests.get(fruit_url,headers=g_headers)
                        res_fruit.encoding = 'utf-8'
                        json_data_fruit = json.loads(res_fruit.text)
                        list_data_fruit = json_data_fruit['rows']
                        for data_fruit in list_data_fruit:
                            print(f"三级商品名称:{data_fruit['goodsName']}, 商品id:{data_fruit['id']}")
                            detail_url = g_detail_url.format(data_fruit['id'])
                            detail_res = requests.get(detail_url,headers=g_headers)
                            detail_res.encoding = 'utf-8'
                            json_data_detail = json.loads(detail_res.text)
                            detail_info = json_data_detail['data']
                            print(f"detail_info:{detail_info}")
                            with open(f'data_{get_time_str()}.csv',mode='a+') as f:
                                csv_writer = csv.writer(f)
                                input_1 = data['sortName']
                                input_2 = child['sortName']
                                input_3 = third_child['sortName']
                                input_4 = data_fruit['goodsName']
                                input_5 = data_fruit['id']
                                input_6 = detail_info['shopName']
                                input_7 = detail_info['inventory']
                                input_8 = detail_info['grossWeight']
                                input_9 = detail_info['suttle']
                                input_10 = detail_info['nowPrice']
                                input_11 = float(input_10) + float(input_8)*0.3 + 2
                                input_12 = 'None'
                                input_13 = float(input_11)/0.7
                                input_14 = 'None'
                                input_15 = input_13 * 0.05
                                input_16 = input_13 - input_11 - input_15
                                input_17 = input_16 / input_13
                                input_18 = 'None'
                                input_19 = 'None'
                                input_20 = 'None'
                                input_21 = detail_info['goodsInstruction']
                                input_22 = detail_info['goodsAttributeInfoDO']['freeAfterSales']
                                input_23 = detail_info['goodsCover']
                                input_24 = detail_info['goodsImage']
                                input_25 = detail_info['goodsVideo']
                                csv_writer.writerow([str(input_1),
                                                     str(input_2),
                                                     str(input_3),
                                                     str(input_4),
                                                     str(input_5),
                                                     str(input_6),
                                                     str(input_7),
                                                     str(input_8),
                                                     str(input_9),
                                                     str(input_10),
                                                     str(input_11),
                                                     str(input_12),
                                                     str(input_13),
                                                     str(input_14),
                                                     str(input_15),
                                                     str(input_16),
                                                     str(input_17),
                                                     str(input_18),
                                                     str(input_19),
                                                     str(input_20),
                                                     str(input_21),
                                                     str(input_22),
                                                     str(input_23),
                                                     str(input_24),
                                                     str(input_25),])
                                print('csv文件写入成功！')
                                
                                
                                
                else:
                    fruit_url = g_fruit_url.format(child['id'], child['sortLevel'],1)
                    res_fruit = requests.get(fruit_url,headers=g_headers)
                    res_fruit.encoding = 'utf-8'
                    json_data_fruit = json.loads(res_fruit.text)
                    list_data_fruit = json_data_fruit['rows']
                    for data_fruit in list_data_fruit:
                        print(f"二级商品名称:{data_fruit['goodsName']}, 商品id:{data_fruit['id']}")
                        detail_url = g_detail_url.format(data_fruit['id'])
                        detail_res = requests.get(detail_url,headers=g_headers)
                        detail_res.encoding = 'utf-8'
                        json_data_detail = json.loads(detail_res.text)
                        detail_info = json_data_detail['data']
                        print(f"创建时间:{detail_info['createTime']}")
                    
    


def write_headers():
    with open(f'data_{get_time_str()}.csv',mode='a+') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(['一级菜单名称','二级菜单名称','三级菜单名称','详细商品名称','商品ID','商家',
                             '剩余','毛重','净重','单价','成本价',
                             '成本单价','报价','报价单价',
                             '人物场','利润','利润率','产地',
                             '货源','等级',
                             '商品说明','售后情况',
                             '封面图片','商品图片','视频地址'])


def run():
    write_headers()
    get_menu_info()


if __name__ == '__main__':
    print('Hello, Begin')
    run()