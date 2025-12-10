import datetime
import socket
import struct
from http.client import responses
from time import sleep

UDP_IP = "10.1.4.46"
UDP_PORT = 10068
TEST_STR_START = 'eb55000100000030420f0000040000b442000000000000000000000000000000000000000000000000000000000000000000000000000000000000e9f17b9bfefc4d40a796adf545523e400000fa43000096430000a041c865a8c0000000000000000000000000000000000000000000000000000000000050196d38100e000000000000ffffff00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000dcedaa'
TEST_STR_START = 'eb550001000000c8410f0000040000b442000000000000000000000000000000000000000000000000000000000000000000000000000000000000e9f17b9bfefc4d40a796adf545523e400000fa43000096430000a041c865a8c0000000000000000000000000000000000000000000000000000000000050196d38100e000000000000ffffff0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000073edaa'
TEST_STR_STOP =  'eb55000100000030420f0000000000b442000000000000000000000000000000000000000000000000000000000000000000000000000000000000e9f17b9bfefc4d40a796adf545523e400000fa43000096430000a041c865a8c0000000000000000000000000000000000000000000000000000000000050196d38100e000000000000ffffff00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000d8edaa'
TEST_STR_QUERY = 'eb55000101000030420f0000000000b442000000000000000000000000000000000000000000000000000000000000000000000000000000000000e9f17b9bfefc4d40a796adf545523e400000fa43000096430000a041c865a8c0000000000000000000000000000000000000000000000000000000000050196d38100e000000000000ffffff00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000d9edaa'
# TEST_STR_QUERY = 'eb55000101000020420f000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000004843000000000000a041c865a8c0000000000000000000000000000000000000000000000000000000000050196d38100e000000000000ffffff00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000ddedaa'
MESSAGE = bytes.fromhex(TEST_STR_START)

print("UDP target IP: %s" % UDP_IP)
print("UDP target port: %s" % UDP_PORT)
print("message: %s" % MESSAGE)

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
# start SPOOFER
# sock.sendto(MESSAGE, (UDP_IP, UDP_PORT)) # START spoofer
# end

# sleep(3)

# STOP spoofer
MESSAGE = bytes.fromhex(TEST_STR_STOP)
# sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))  # STOP spoofer
# end


MESSAGE_QUERY = bytes.fromhex(TEST_STR_QUERY)
with sock as s:
    sock.sendto(MESSAGE_QUERY, (UDP_IP, UDP_PORT))
    print('Отправил:', MESSAGE_QUERY.hex())
    data = s.recv(1024)
print('Получил: ', data.hex())

response = data.hex()
print(f'{response[0:4]} - header') # header 'eb55'
print(f'{response[4:8]} - lenght 256 bytes always') # lenght 256 bytes always '0001'
print(f'{response[8:10]} - Fixed "f1"') # Fixed "f1"
print(f'{response[10:18]} - {struct.unpack("<f", bytes.fromhex(response[10:18]))[0]:.2f} - current power, дБм') # current power, дБм
print(f'{response[18:26]} - {struct.unpack("<f", bytes.fromhex(response[18:26]))[0]:.2f} - minimum power allowed power, дБм') # minimum power allowed power, дБм
print(f'{response[26:34]} - {struct.unpack("<f", bytes.fromhex(response[26:34]))[0]:.2f} - maximum power allowed power, дБм') # maximum power allowed power, дБм
gnss_systems = struct.unpack("<h", bytes.fromhex(response[34:38]))[0]
is_GPS_on = bin(gnss_systems)[-1]
is_BDS_on = bin(gnss_systems)[-2]
is_GLONASS_on = bin(gnss_systems)[-3]
is_GALILEO_on = bin(gnss_systems)[-4]
print(f'{response[34:38]} - {gnss_systems:04x} - {gnss_systems:04b} - Используемые системы ГНСС') # GNSS systems 0 bit - GPS, 1 bit - BDS, 2 bit - GLO, 3 bit - GAL
print(f'- GPS - {'ВКЛ' if is_GPS_on == '1' else 'ВЫКЛ'}')
print(f'- BeiDou - {'ВКЛ' if is_BDS_on == '1' else 'ВЫКЛ'}')
print(f'- ГЛОНАСС - {'ВКЛ' if is_GLONASS_on == '1' else 'ВЫКЛ'}')
print(f'- GALILEO - {'ВКЛ' if is_GALILEO_on == '1' else 'ВЫКЛ'}')
print(f'{response[38:40]} - RESERVED') # RESERVED
print(f'{response[40:42]} - Decoy launch switch status') # Decoy launch switch status
print(f'{response[42:44]} - Sat receiving status') # Sat receiving status, not receiving when transmitting
print(f'{response[44:46]} - {int(response[44:46], 16)} - Общее количество принимаемых спутников') # Number of all receiving local satellites
print(f'{response[46:62]} - {struct.unpack("<d", bytes.fromhex(response[46:62]))[0]:.5f}° - Широта устройства') # Широта устройства
print(f'{response[62:78]} - {struct.unpack("<d", bytes.fromhex(response[62:78]))[0]:.5f}° - Долгота устройства') # Долгота устройства
print(f'{response[78:86]} - {struct.unpack("<f", bytes.fromhex(response[78:86]))[0]:.2f}м - Высота устройства') # Высота устройства
print(f'{response[86:88]} - {'НЕДОСТУПЕН' if response[86:88] == '00' else 'Доступен' if response[86:88] == '01' else "НЕИЗВЕСТНО"} - Clock quality') # Clock quality, 0-unavailable, 1-available
print(f'{response[88:90]} - {'Ошибка' if response[88:90] == '00' else 'OK' if response[88:90] == '01' else "НЕИЗВЕСТНО"} - RF status') # RF status, 0-abnormal, 1-normal
print(f'{response[90:92]} - {int(response[90:92], 16)} - GPS, Кол-во симулируемых спутников') # GPS, Кол-во симулируемых спутников
print(f'{response[92:94]} - {int(response[92:94], 16)} - BeiDou, Кол-во симулируемых спутников') # GPS, Кол-во симулируемых спутников
print(f'{response[94:96]} - {int(response[94:96], 16)} - ГЛОНАСС, Кол-во симулируемых спутников') # GPS, Кол-во симулируемых спутников
print(f'{response[96:98]} - {int(response[96:98], 16)} - Galileo, Кол-во симулируемых спутников') # GPS, Кол-во симулируемых спутников
print(f'{response[98:100]} - {int(response[98:100], 16)} - Режим подавления - {'Отклонение' if response[98:100] == '01' else 'Купол' if response[98:100] == '03' else "Помехи" if response[98:100] == '04' else "ВЫКЛ/Неизвестно"}') # Режим подавления, 4-Помехи, 1-отклонение, 3-купол
print(f'{response[100:156]} - RESERVED') # RESERVED
print(f'{response[156:158]} - {int(response[156:158], 16)}° - Температура усилителя мощности') # Температура усилителя мощности
print(f'{response[158:160]} - {int(response[158:160], 16)}В - Напряжение усилителя мощности') # Напряжение усилителя мощности
print(f'{response[160:162]} - {int(response[160:162], 16)}А - Потребление тока усилителя мощности') # Потребление тока усилителя мощности
protection_status = int(response[162:164], 16)
protection_status = 2
print(f'{response[162:164]} - {protection_status:02x} - {protection_status:08b} - Статус защиты') # Protection status
is_alarm = True if format(protection_status, '08b')[-1] == '1' else False # 0 bit - Нет аварий,
is_ant_alarm = True if format(protection_status, '08b')[-3] == '1' else False # 2 bit - Antenna failure,
is_neg_pres_alarm = True if format(protection_status, '08b')[-4] == '1' else False # 3 bit - negative pressure protection ,
is_overcur_alarm = True if format(protection_status, '08b')[-5] == '1' else False # 4 bit - защита от перегрузки по току,
is_und_vol_alarm = True if format(protection_status, '08b')[-6] == '1' else False # 5 bit - низкое напряжение
is_over_vol_alarm = True if format(protection_status, '08b')[-7] == '1' else False # 6 bit - высокое напряжение
is_temp_alarm = True if format(protection_status, '08b')[-8] == '1' else False # 7 bit - высокая температура
print(f'- Авария - {'Нет' if not is_alarm else 'ЕСТЬ'}')
print(f'- Антенна - {'Нет' if not is_ant_alarm else 'ЕСТЬ'}')
print(f'- Neg Pressure - {'Нет' if not is_neg_pres_alarm else 'ЕСТЬ'}')
print(f'- Перегрузка по току - {'Нет' if not is_overcur_alarm else 'ЕСТЬ'}')
print(f'- Низкое напряжение - {'Нет' if not is_und_vol_alarm else 'ЕСТЬ'}')
print(f'- Высокое напряжение - {'Нет' if not is_over_vol_alarm else 'ЕСТЬ'}')
print(f'- Высокая температура  - {'Нет' if not is_temp_alarm else 'ЕСТЬ'}')
print(f'{response[164:168]} - {struct.unpack("<h", bytes.fromhex(response[164:168]))[0]/10:.2f} - Мощность усилителя, дБм') # Мощность усилителя, дБм
print(f'{response[168:170]} - RESERVED') # RESERVED
print(f'{response[170:186]} - {struct.unpack("<d", bytes.fromhex(response[170:186]))[0]:.5f}° - Широта центра купола') # Широта центра купола
print(f'{response[186:202]} - {struct.unpack("<d", bytes.fromhex(response[186:202]))[0]:.5f}° - Долгота центра купола') # Долгота центра купола
print(f'{response[202:210]} - {struct.unpack("<f", bytes.fromhex(response[202:210]))[0]:.2f}м - Высота центра купола') # Высота центра купола
print(f'{response[210:218]} - {struct.unpack("<f", bytes.fromhex(response[210:218]))[0]:.2f}м - Радиус купола') # Радиус купола
print(f'{response[218:226]} - {struct.unpack("<f", bytes.fromhex(response[218:226]))[0]:.2f}м/c - Скорость купола') # Скорость купола
unknown_time = struct.unpack("<I", bytes.fromhex(response[226:234]))[0]
print(f'{response[226:234]} - {unknown_time} {datetime.datetime.fromtimestamp(unknown_time)} - Время UNIX ??') # Время UNIX timestamp ??? непонятно
print(f'{response[234:238]} - {struct.unpack("<h", bytes.fromhex(response[234:238]))[0]} - Интервал синхронизации времени') # Интервал синхронизации времени
time_source = int(response[238:240], 16)
print(f'{response[238:240]} - {'Спутник' if time_source == 0 else 'NTP' if time_source == 1 else 'Напрямую с компьютера' if time_source == 2 else 'Неизвестно'} - Источник времени') # Источник времени
freq_points = struct.unpack("<I", bytes.fromhex(response[240:248]))[0]
is_GPS_L1CA = True if format(freq_points, '016b')[-1] == '1' else False # 0 bit - GPS L1C/A,
is_BDS_B1I = True if format(freq_points, '016b')[-2] == '1' else False # 0 bit - BDS B1I,
is_GLONASS_L1 = True if format(freq_points, '016b')[-3] == '1' else False # 0 bit - ГЛОНАСС L1,
is_GAL_E1 = True if format(freq_points, '016b')[-4] == '1' else False # 0 bit - Galileo E1,
is_GPS_L2C = True if format(freq_points, '016b')[-5] == '1' else False # 0 bit - GPS L2C,
is_GPS_L5C = True if format(freq_points, '016b')[-6] == '1' else False # 0 bit - GPS L5C,
is_BDS_L2I = True if format(freq_points, '016b')[-7] == '1' else False # 0 bit - BDS L2I,
is_GLONASS_L2 = True if format(freq_points, '016b')[-8] == '1' else False # 0 bit - ГЛОНАСС L2,
is_QZSS_L1CA = True if format(freq_points, '016b')[-9] == '1' else False # 0 bit - QZSS L1C/A,
is_GAL_E5A = True if format(freq_points, '016b')[-10] == '1' else False # 0 bit - Galileo E5A,
print(f'{response[240:248]} - {freq_points:04x} - {freq_points:016b} - Поддерживаемые системы и частоты') # Поддерживаемые системы и частоты
print(f'- GPS L1C/A - {'Да' if is_GPS_L1CA else 'НЕТ'}')
print(f'- BDS B1I - {'Да' if is_BDS_B1I else 'НЕТ'}')
print(f'- ГЛОНАСС L1 - {'Да' if is_GLONASS_L1 else 'НЕТ'}')
print(f'- Galileo E1 - {'Да' if is_GAL_E1 else 'НЕТ'}')
print(f'- GPS L2C - {'Да' if is_GPS_L2C else 'НЕТ'}')
print(f'- GPS L5C - {'Да' if is_GPS_L5C else 'НЕТ'}')
print(f'- BDS L2I - {'Да' if is_BDS_L2I else 'НЕТ'}')
print(f'- ГЛОНАСС L2 - {'Да' if is_GLONASS_L2 else 'НЕТ'}')
print(f'- QZSS L1C/A - {'Да' if is_QZSS_L1CA else 'НЕТ'}')
print(f'- Galileo E5A - {'Да' if is_GAL_E5A else 'НЕТ'}')
cur_time = struct.unpack("<I", bytes.fromhex(response[248:256]))[0]
print(f'{response[248:256]} - {cur_time} - {datetime.datetime.fromtimestamp(cur_time)} - Текущее время UNIX') # Текущее время UNIX timestamp
mask = response[256:264]
octet_list = [str(int(mask[i:i+2], 16)) for i in range(0, len(mask), 2)]
octet_list.reverse()
mask_int = '.'.join(octet_list)
print(f'{response[256:264]} - {mask_int} - Маска') # маска
print(f'{response[264:266]} - {'Да' if response[264:266] == '01' else 'НЕТ' if response[264:266] == '00' else 'Неизвестно'} - Память последнего состояния RF Switch') # Память последнего состояния RF Switch
print(f'{response[266:268]} - {'Да' if response[266:268] == '01' else 'НЕТ' if response[266:268] == '00' else 'Неизвестно'} - Поиск спутников при активной передаче') # Поиск спутников при активной передаче
print(f'{response[268:270]} - RESERVED') # RESERVED
print(f'{response[270:506]} - RESERVED') # RESERVED
print(f'{response[506:508]} - Контрольная сумма') # cum sum
print(f'{response[508:512]} - Конец фрейма') # Конец фрейма edaa
