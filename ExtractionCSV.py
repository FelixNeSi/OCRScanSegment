import pandas as pd

df_suffix = pd.read_csv('adv_trade_suffixes.csv')
df_other_trades = pd.read_csv('Other Trades (AdvTrades).csv')

all_suffix = df_suffix['suffixes'].tolist()
all_other_tradez = df_other_trades['other trades']
all_other_trades = [t.strip().lower() for t in all_other_tradez]
# all_other_trades = list( dict.fromkeys(all_other_trades) )
all_other_tradess = list(set(all_other_trades))
print(len(all_other_trades))
print(all_suffix)

df = pd.read_csv('adv_trade_v1.csv')
adv_trade1 = df['Adv_trade1'].tolist()
adv_trade2 = df['Adv_trade2'].tolist()

print(adv_trade1[0].split(','))

combined_adv_trade = []

for i, trade in enumerate(adv_trade1):
    temp_trade = trade
    if not isinstance(adv_trade2[i], float):
        temp_trade = temp_trade + " , " + adv_trade2[i]
        # print(adv_trade2[i])
    combined_adv_trade.append(temp_trade)

# print(combined_adv_trade[187])

suffixes = []
other_trades = []

for i, trade in enumerate(combined_adv_trade):
    # print("++++++++")
    temp_suffix = []
    temp_other_trade = []
    if not isinstance(trade, float):
        # trade = trade.center(len(trade) + 2)
        trade = trade.replace(';', ',')
        temp_split = trade.split(',')
        for split in temp_split:
            # split = split.center(len(split) + 2)
            for suffix in all_suffix:
                # print(split, '_+++', suffix)
                if suffix.lower() in split.lower():
                    # print(split.lower() , "+++ ", suffix.lower())
                    # temp_suffix = split.strip() + ", " + temp_suffix

                    tmp_suffix = split.lower().strip().replace(suffix.lower(), "")
                    if len(tmp_suffix) > 1:
                        temp_suffix.append('{} ({})'.format(suffix, tmp_suffix))
                    else:
                        temp_suffix.append('{}'.format(suffix))

            for j, other_trade in enumerate(all_other_tradess):
                if other_trade.lower() in split.lower():
                    # temp_other_trade = split.strip() + ", " + temp_other_trade
                    # print(other_trade)
                    print("FOUND {} AT INDEX {}, ITERATION {}, OTHER TRADE {}".format(split, str(i), str(j), other_trade))
                    tmp_other_trade = split.lower().strip().replace(other_trade.lower(), "")
                    if len(tmp_other_trade) > 1:
                        temp_other_trade.append('{} ({})'.format(other_trade, tmp_other_trade))
                    else:
                        temp_other_trade.append('{}'.format(other_trade))
                    # # print(split.lower() , "+++", other_trade.lower())
                    # print("+++++++++++++++")
                    # print("FOUND TRADE {}".format(other_trade))
                    # temp_other_trade = split.strip()
                    # print("FULL TEXT {}".format(split.strip()))
                    # print("FULL TEXT, TEMP OTHER TRADE {}".format(temp_other_trade))
                    # trade_to_remove = temp_other_trade.lower()
                    # trade_to_remove = trade_to_remove.replace(other_trade.lower(), '')
                    # # temp_other_trade_removed = temp_other_trade.lower().replace(other_trade.lower(), '')
                    # print("TEMP OTHER TRADE REMOVED {}".format(trade_to_remove))
                    # # temp_other_trade = other_trade + ' (' + trade_to_remove + '), ' + temp_other_trade
                    # # temp_other_trade = other_trade + ' ({})'.format(temp_other_trade_removed) + ", "
                    # if len(trade_to_remove.strip()) > 1:
                    #     # temp_other_trade = other_trade + ' (' + trade_to_remove + '), ' + temp_other_trade
                    #     # temp_other_trade = '{}, {} ({}), '.format(temp_other_trade, other_trade, trade_to_remove)
                    # else:
                    #     temp_other_trade = other_trade + ', ' + temp_other_trade
                    #     temp_other_trade = '{}, {}, '.format(temp_other_trade, other_trade)

    # suffixes.append(temp_suffix[:-2])
    tmp_save_suffix = ', '.join(temp_suffix)
    tmp_trades = ', '.join(temp_other_trade)
    suffixes.append(tmp_save_suffix)
    other_trades.append(tmp_trades)

df.insert(8, "Suffixes", suffixes, allow_duplicates=True)
df.insert(9, "Other Trades", other_trades, allow_duplicates=True)

df.to_csv("adv_trade_v6.csv", index=False)



# import pandas as pd
#
# df = pd.read_csv('Advertised Trade.csv')
# adv_trade1 = df['Adv_trade1'].tolist()
# adv_trade2 = df['Adv_trade2'].tolist()
#
# print(adv_trade1[0].split(','))
#
# combined_adv_trade = []
#
# for i, trade in enumerate(adv_trade1):
#     temp_trade = trade
#     if not isinstance(adv_trade2[i], float):
#         temp_trade = temp_trade + " , " + adv_trade2[i]
#         # print(adv_trade2[i])
#     combined_adv_trade.append(temp_trade)
#
# # print(combined_adv_trade[187])
#
# seller, maker, i_maker, i_seller = [], [], [], []
#
# for i, trade in enumerate(combined_adv_trade):
#     temp_seller, temp_maker, temp_i_maker, temp_i_seller = '', '', '', ''
#     if not isinstance(trade, float):
#         # trade = trade.center(len(trade) + 2)
#         trade = trade.replace(';', ',')
#         temp_split = trade.split(',')
#         for split in temp_split:
#             split = split.center(len(split) + 2)
#             if ' M ' in split or ' Maker ' in split:
#                 split = split.replace(' M ', '')
#                 split = split.replace(' Maker ', '')
#                 temp_maker = split.strip() + ", " + temp_maker
#             if ' S ' in split or ' Seller ' in split:
#                 split = split.replace(' S ', '')
#                 split = split.replace(' Seller ', '')
#                 temp_seller = split.strip() + ", " + temp_seller
#             if ' IM ' in split or ' Instrument Maker ' in split:
#                 split = split.replace(' IM ', '')
#                 split = split.replace(' Instrument Maker ', '')
#                 temp_i_maker = split.strip() + ", " + temp_i_maker
#             if ' IS ' in split or ' Instrument Seller ' in split:
#                 split = split.replace(' IS ', '')
#                 split = split.replace(' Instrument Seller ', '')
#                 temp_i_seller = split.strip() + ", " + temp_i_seller
#     seller.append(temp_seller[:-2])
#     maker.append(temp_maker[:-2])
#     i_seller.append(temp_i_seller[:-2])
#     i_maker.append(temp_i_maker[:-2])
#
# df.insert(4, "Maker", maker, allow_duplicates=True)
# df.insert(5, "Instrument Maker", i_maker, allow_duplicates=True)
# df.insert(6, "Seller", seller, allow_duplicates=True)
# df.insert(7, "Instrument Seller", i_seller, allow_duplicates=True)
#
# df.to_csv("adv_trade_v1.csv", index=False)