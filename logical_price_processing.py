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
