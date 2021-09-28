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
    def clear_price(data):
        if data != 0:
            d = data.replace(' ', '').replace('₽', '')
        else:
            d = 0
        return d

    def clear_discount(data):
        rub_re = '''[\d ]{4,8}'''
        reg_fa1 = '''[\d– ]{4,9}р. при оплате онлайн HOME[\d]{1,5}'''
        reg_fa2 = '''[\d– ]{4,9}р. по промокоду HOME[\d]{1,5}'''
        list_reg = [reg_fa1, reg_fa2]
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
            pr = int(i)
            if pr > amount_discounts:
                amount_discounts = pr

        return amount_discounts

    dict_local = {}
    for name_product, value in price_dict_entrance.items():
        price_product = clear_price(value[0])
        discount_product = clear_discount(value[1])
        dict_local[name_product] = price_product
    return dict_local


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


def logical_price_processing_mvm(data):
    def is_none(pr1):
        if pr1 is not None:
            r = int(value[0])
        else:
            r = 0
        return r

    dict_local = {}
    for article, value in data.items():
        price_1, price_2 = is_none(value[0]), is_none(value[1])

        if price_1 > 0:
            if price_1 > price_2 > 0:
                price = price_2
            else:
                price = price_1
            dict_local[article] = price
    return dict_local
