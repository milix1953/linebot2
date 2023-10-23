import pymongo

# 要獲得mongodb網址，請至mongodb網站申請帳號進行資料庫建立，網址　https://www.mongodb.com/
# 獲取的網址方法之範例如圖： https://i.imgur.com/HLCk99r.png
client = pymongo.MongoClient("自己的mongodb連線網址")

#第一個db的建立
db = client['MongoClient']
col = db['Database']

# 為用戶菜單創建一個新的collection
menu_col = db['UserMenu']

#判斷key是否在指定的dictionary當中，若有則return True
def dicMemberCheck(key, dicObj):
    if key in dicObj:
        return True
    else:
        return False

#寫入資料data是dictionary
def write_one_data(data):
    col.insert_one(data)

#寫入多筆資料，data是一個由dictionary組成的list
def write_many_datas(data):
    col.insert_many(data)

#讀取所有LINE的webhook event紀錄資料
def read_many_datas():
    data_list = []
    for data in col.find():
        data_list.append(str(data))

    print(data_list)
    return data_list

#讀取LINE的對話紀錄資料
def read_chat_records():
    data_list = []
    for data in col.find():
        if dicMemberCheck('events',data):
            if dicMemberCheck('message',data['events'][0]):
                if dicMemberCheck('text',data['events'][0]['message']):
                    print(data['events'][0]['message']['text'])
                    data_list.append(data['events'][0]['message']['text'])
        else:
            print('非LINE訊息',data)

    print(data_list)
    return data_list

#刪除所有資料
def delete_all_data():
    data_list = []
    for x in col.find():
        data_list.append(x)   

    datas_len = len(data_list)

    col.delete_many({})

    if len(data_list)!=0:
        return f"資料刪除完畢，共{datas_len}筆"
    else:
        return "資料刪除出錯"

#找到最新的一筆資料
def col_find(key):
    for data in col.find({}).sort('_id',-1):
        if dicMemberCheck(key,data):
            data = data[key]
            break
    print(data)
    return data

# 添加一個新的菜單項目
def add_menu_item(user_id, menu_item):
    menu_data = menu_col.find_one({'user_id': user_id})
    if menu_data:
        # 如果用戶已經有菜單，則添加新的菜單項目
        if 'menu_items' not in menu_data:
            menu_data['menu_items'] = []
        if menu_item not in menu_data['menu_items']:
            menu_data['menu_items'].append(menu_item)
            menu_col.update_one({'user_id': user_id}, {'$set': {'menu_items': menu_data['menu_items']}})
    else:
        # 如果用戶還沒有菜單，則創建一個新的菜單
        menu_data = {
            'user_id': user_id,
            'menu_items': [menu_item]
        }
        menu_col.insert_one(menu_data)

# 刪除一個菜單項目
def delete_menu_item(user_id, menu_item):
    menu_data = menu_col.find_one({'user_id': user_id})
    if menu_data and 'menu_items' in menu_data and menu_item in menu_data['menu_items']:
        menu_data['menu_items'].remove(menu_item)
        menu_col.update_one({'user_id': user_id}, {'$set': {'menu_items': menu_data['menu_items']}})

# 獲取用戶的菜單
def get_user_menu(user_id):
    menu_data = menu_col.find_one({'user_id': user_id})
    if menu_data and 'menu_items' in menu_data:
        return menu_data['menu_items']
    return []

if __name__ == '__main__':
    print(read_many_datas())
