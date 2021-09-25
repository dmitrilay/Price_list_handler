import re


def ProverkaNaChislo(V_skidka):
    V2_skidka = 0
    try:
        if V_skidka != None:
            V2_skidka = int(V_skidka)
    except Exception:
        pass
    return V2_skidka


def logical_price_processing_mts(price_dict_entrance):
    price_dict_exit = {'Наименование': [], 'Цена': []}
    for i in range(0, len(price_dict_entrance['Наименование'])):
        V_Price_p1 = ProverkaNaChislo(V_skidka=price_dict_entrance['Цена_1'][i])
        if V_Price_p1 != 0:
            V_Skid1 = ProverkaNaChislo(V_skidka=price_dict_entrance['Скидка_1'][i])
            V_Skid2 = ProverkaNaChislo(V_skidka=price_dict_entrance['Скидка_2'][i])
            if V_Skid1 != 0 or V_Skid2 != 0:
                if V_Skid1 >= V_Skid2:
                    p1 = V_Price_p1 - V_Skid1
                elif V_Skid1 <= V_Skid2:
                    p1 = V_Price_p1 - V_Skid2
                else:
                    p1 = 0
            else:
                p1 = V_Price_p1

            price_dict_exit['Наименование'].append(price_dict_entrance['Наименование'][i])
            price_dict_exit['Цена'].append(p1)
            p1 = 0
    return price_dict_exit


def logical_price_processing_dns(price_dict_entrance):
    def clear_name(data):
        """Очистка наименования от [лишних значений]"""
        end = data.find('[') - 1
        return data[0:end]

    def clear_price(data):
        pr = data.replace(' ', '').replace('₽', '')
        data = list(pr.split('\n'))
        data = int(data[0])
        return data

    def clear_discount(data):
        rub_re = '''[\d ]{4,8}'''
        reg_fa1 = '''Рассрочка [\d-]{1,6} или Выгода [\d ]{1,8}₽'''
        reg_fa2 = '''Скидка за онлайн оплату [\d ]{1,8}₽'''
        list_reg = [reg_fa2]
        discount = []
        if data is not None:
            promo = data.split(';')
            for i in promo:
                for reg_fa in list_reg:
                    regex_num = re.search(reg_fa, i)
                    if regex_num:
                        discount.append(re.search(rub_re, regex_num[0])[0].replace(' ', ''))
        amount_discounts = 0
        for i in discount:
            amount_discounts += (int(i))
        return amount_discounts

    dict_local = {}
    for key, value in price_dict_entrance.items():
        name_product = clear_name(key)
        price_product = clear_price(value[0])
        discount_product = clear_discount(value[1])
        dict_local[name_product] = price_product - discount_product
    return dict_local
