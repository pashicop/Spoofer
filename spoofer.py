import struct


test_circle_command = 'eb55000100000030420f00006700000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000e9f17b9bfefc4d40a796adf545523e400000fa43000096430000a041c865a8c0000000000000000000000000000000000000000000000000000000000050196d38100e000000000000ffffff0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000049edaa'


def get_power(power_sp):
     return struct.pack('<f', power_sp).hex()


def get_coordinates(lat, long):
    return (struct.pack('<d', lat).hex() +
            struct.pack('<d', long).hex())


def get_height(height_drone):
    return struct.pack('<f', height_drone).hex()


def get_radius(radius_circle):
    return struct.pack('<f', radius_circle).hex()


def get_speed(speed_drone):
    return struct.pack('<f', speed_drone).hex()


def get_hex_from_ip_or_mask(ip='192.168.101.200'):
    ip_hex = ''
    octet_list = ip.split('.')
    octet_list.reverse()
    for octet in octet_list:
        ip_hex += format(int(octet), '02x')
    return ip_hex


def get_time(t='50196d38'):
    return t


def get_time_synchro_interval(interval=3600):
    return struct.pack('<h', interval).hex()


def get_sum(string):
    int_list = [int(string[i:i + 2], 16) for i in range(0, len(string), 2)]
    cur_sum = 0
    for cur_int in int_list:
        cur_sum += cur_int
    return hex(cur_sum)[-2:]


def generate_command(m, p, x_c=None, y_c=None, height_c=None, radius_c=None, speed_c=None, az=None):
    command = ''
    if m == 'circle':
        command = 'eb55' # add header
        command += '0001' # add lenght ALWAYS 256 bytes
        command += '00' # set
        command += get_power(p) # add power in float LE
        command += '0f00' # add all GNSS systems: GPS BDS Glonass Galileo
        command += '00' # RESERVED
        command += '67' # for circle? shoud be 03?
        command += '00' * 46 # RESERVED 46 bytes
        command += get_coordinates(x_c, y_c) # add latitude and longitude in Double LE
        command += get_height(height_c) # add height in float LE
        command += get_radius(radius_c) #add circle radius in float LE
        command += get_speed(speed_c) # add drone speed in float LE
        command += get_hex_from_ip_or_mask('192.168.101.200') # not needed for circle IP
        command += '00' * 29  # RESERVED 29 bytes
        command += get_time() # not needed
        command += get_time_synchro_interval() # not needed
        command += '00' * 5 # not needed timing source conf
        command += get_hex_from_ip_or_mask('255.255.255.0') # not needed MASK
        command += '00' # memory last state
        command += '00' # disable CA code noise
        command += '00' * 116  # RESERVED 116 bytes
        command += get_sum(command) # last byte of command sum
        command += 'edaa' # end frame
    # elif m == 'disperse':
    #     command = 'eb55'  # add header
    #     command += '0001'  # add lenght ALWAYS 256 bytes
    #     command += '00'  # set
    #     command += get_power(p)  # add power in float LE
    #     command += '0f00'  # add all GNSS systems: GPS BDS Glonass Galileo
    #     command += '00'  # RESERVED
    #     command += '67'  # for circle? shoud be 03?
    #     command += '00' * 46  # RESERVED 46 bytes
    #     command += get_coordinates(x_c, y_c)  # add latitude and longitude in Double LE
    #     command += get_height(height_c)  # add height in float LE
    #     command += get_radius(radius_c)  # add circle radius in float LE
    #     command += get_speed(speed_c)  # add drone speed in float LE
    #     command += get_hex_from_ip_or_mask('192.168.101.200')  # not needed for circle IP
    #     command += '00' * 29  # RESERVED 29 bytes
    #     command += get_time()  # not needed
    #     command += get_time_synchro_interval()  # not needed
    #     command += '00' * 5  # not needed timing source conf
    #     command += get_hex_from_ip_or_mask('255.255.255.0')  # not needed MASK
    #     command += '00'  # memory last state
    #     command += '00'  # disable CA code noise
    #     command += '00' * 116  # RESERVED 116 bytes
    #     command += get_sum(command)  # last byte of command sum
    #     command += 'edaa'  # end frame
    return command


def main():
    x = 59.97652
    y = 30.32138
    height = 500
    radius = 300
    speed = 20
    power = 44
    azimut = 90
    mode = ['jamming', 'disperse', 'circle']
    print(f'{'-' * 40}')
    print(f'| Режим Купол с параметрами:'.ljust(40))
    print(f'| Мощность: {power} {'дБм'.ljust(40)}|')
    print(f'| Координаты: {x}, {y}')
    print(f'| Радиус: {radius} м')
    print(f'| Высота: {height} м')
    print(f'| Скорость: {speed} м/с')
    print(f'{'-' * 40}')
    print(f'{'Тестовая строка:'.ljust(23)} {test_circle_command}')
    result_command = generate_command(mode[2], power, x, y, height, radius, speed)
    print(f'{'Сгенерированная строка:'.ljust(23)} {result_command}')
    if test_circle_command == result_command:
        print('Команды совпадают!')
    else:
        print('ОШИБКА!! Команды НЕ СОВПАДАЮТ')


if __name__ == "__main__":
    main()