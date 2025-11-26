import struct


test_circle_config_command = 'eb55000100000030420f0000670000b442000000000000000000000000000000000000000000000000000000000000000000000000000000000000e9f17b9bfefc4d40a796adf545523e400000fa43000096430000a041c865a8c0000000000000000000000000000000000000000000000000000000000050196d38100e000000000000ffffff000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000003fedaa'
test_start_circle_command = 'eb55000100000030420f0000030000b442000000000000000000000000000000000000000000000000000000000000000000000000000000000000e9f17b9bfefc4d40a796adf545523e400000fa43000096430000a041c865a8c0000000000000000000000000000000000000000000000000000000000050196d38100e000000000000ffffff00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000dbedaa'
test_start_disperse_command = 'eb55000100000030420f0000010000b442000000000000000000000000000000000000000000000000000000000000000000000000000000000000e9f17b9bfefc4d40a796adf545523e400000fa43000096430000a041c865a8c0000000000000000000000000000000000000000000000000000000000050196d38100e000000000000ffffff00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000d9edaa'
test_start_jamming_command = 'eb55000100000030420f0000040000b442000000000000000000000000000000000000000000000000000000000000000000000000000000000000e9f17b9bfefc4d40a796adf545523e400000fa43000096430000a041c865a8c0000000000000000000000000000000000000000000000000000000000050196d38100e000000000000ffffff00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000dcedaa'
test_stop_command = 'eb55000100000030420f0000000000b442000000000000000000000000000000000000000000000000000000000000000000000000000000000000e9f17b9bfefc4d40a796adf545523e400000fa43000096430000a041c865a8c0000000000000000000000000000000000000000000000000000000000050196d38100e000000000000ffffff00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000d8edaa'


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


def get_azimuth(az):
    return struct.pack('<f', az).hex()


def get_sum(string):
    int_list = [int(string[i:i + 2], 16) for i in range(0, len(string), 2)]
    cur_sum = 0
    for cur_int in int_list:
        cur_sum += cur_int
    return hex(cur_sum)[-2:]


# def generate_command(m, p, x_c=None, y_c=None, height_c=None, radius_c=None, speed_c=None, az=None):
def generate_command(**parameters):
    # for key, value in parameters.items():
    #     print(f'{key} - {value}')
    command = ''
    if parameters.get('sp_mode') == 'circle_pars' or parameters.get('sp_mode') == 'start_circle':
        command = 'eb55' # add header
        command += '0001' # add lenght ALWAYS 256 bytes
        command += '00' # set
        command += get_power(parameters.get('sp_power', 44)) # add power in float LE
        command += '0f00' # add all GNSS systems: GPS BDS Glonass Galileo
        command += '00' # RESERVED
        if parameters.get('sp_mode') == 'circle_pars':
            command += '67' # for circle parameters
        else:
            command += '03'  # for start circle
        command += get_azimuth(parameters.get('sp_azimuth', 90))  # add azimuth
        command += '00' * 42 # RESERVED 46 bytes
        command += get_coordinates(parameters.get('sp_x', 60), parameters.get('sp_y', 30)) # add latitude and longitude in Double LE
        command += get_height(parameters.get('sp_height', 500)) # add height in float LE
        command += get_radius(parameters.get('sp_radius', 300)) #add circle radius in float LE
        command += get_speed(parameters.get('sp_speed', 20)) # add drone speed in float LE
        command += get_hex_from_ip_or_mask(parameters.get('sp_ip', '192.168.101.200')) # not needed for circle IP
        command += '00' * 29  # RESERVED 29 bytes
        command += get_time() # not needed
        command += get_time_synchro_interval() # not needed
        command += '00' * 5 # not needed timing source conf
        command += get_hex_from_ip_or_mask(parameters.get('sp_mask', '255.255.255.0')) # not needed MASK
        command += '00' # memory last state
        command += '00' # disable CA code noise
        command += '00' * 116  # RESERVED 116 bytes
        command_sum = get_sum(command) # calculate command sum
        command += command_sum # last byte of command sum
        command += 'edaa' # end frame
    elif parameters.get('sp_mode') == 'disperse':
        command = 'eb55'  # add header
        command += '0001'  # add lenght ALWAYS 256 bytes
        command += '00'  # set
        command += get_power(parameters.get('sp_power', 44))  # add power in float LE
        command += '0f00'  # add all GNSS systems: GPS BDS Glonass Galileo
        command += '00'  # RESERVED
        command += '01'  # for Disperse
        command += get_azimuth(parameters.get('sp_azimuth', 90))  # add azimuth
        command += '00' * 42  # RESERVED 42 bytes
        command += get_coordinates(parameters.get('sp_x', 59.97652),
                                   parameters.get('sp_y', 30.32138))  # add latitude and longitude in Double LE
        command += get_height(parameters.get('sp_height', 500))  # add height in float LE
        command += get_radius(parameters.get('sp_radius', 300))  # add circle radius in float LE
        command += get_speed(parameters.get('sp_speed', 20))  # add drone speed in float LE
        command += get_hex_from_ip_or_mask(parameters.get('sp_ip', '192.168.101.200'))  # not needed for circle IP
        command += '00' * 29  # RESERVED 29 bytes
        command += get_time()  # not needed
        command += get_time_synchro_interval()  # not needed
        command += '00' * 5  # not needed timing source conf
        command += get_hex_from_ip_or_mask(parameters.get('sp_mask', '255.255.255.0'))  # not needed MASK
        command += '00'  # memory last state
        command += '00'  # disable CA code noise
        command += '00' * 116  # RESERVED 116 bytes
        command_sum = get_sum(command)  # calculate command sum
        command += command_sum  # last byte of command sum
        command += 'edaa'  # end frame
    elif parameters.get('sp_mode') == 'jamming':
        command = 'eb55'  # add header
        command += '0001'  # add lenght ALWAYS 256 bytes
        command += '00'  # set
        command += get_power(parameters.get('sp_power', 44))  # add power in float LE
        command += '0f00'  # add all GNSS systems: GPS BDS Glonass Galileo
        command += '00'  # RESERVED
        command += '04'  # for Jamming
        command += get_azimuth(parameters.get('sp_azimuth', 90))  # add azimuth
        command += '00' * 42  # RESERVED 42 bytes
        command += get_coordinates(parameters.get('sp_x', 59.97652),
                                   parameters.get('sp_y', 30.32138))  # add latitude and longitude in Double LE
        command += get_height(parameters.get('sp_height', 500))  # add height in float LE
        command += get_radius(parameters.get('sp_radius', 300))  # add circle radius in float LE
        command += get_speed(parameters.get('sp_speed', 20))  # add drone speed in float LE
        command += get_hex_from_ip_or_mask(parameters.get('sp_ip', '192.168.101.200'))  # not needed for circle IP
        command += '00' * 29  # RESERVED 29 bytes
        command += get_time()  # not needed
        command += get_time_synchro_interval()  # not needed
        command += '00' * 5  # not needed timing source conf
        command += get_hex_from_ip_or_mask(parameters.get('sp_mask', '255.255.255.0'))  # not needed MASK
        command += '00'  # memory last state
        command += '00'  # disable CA code noise
        command += '00' * 116  # RESERVED 116 bytes
        command_sum = get_sum(command)  # calculate command sum
        command += command_sum  # last byte of command sum
        command += 'edaa'  # end frame
    elif parameters.get('sp_mode') == 'stop':
        command = 'eb55'  # add header
        command += '0001'  # add lenght ALWAYS 256 bytes
        command += '00'  # set
        command += get_power(parameters.get('sp_power', 44))  # add power in float LE
        command += '0f00'  # add all GNSS systems: GPS BDS Glonass Galileo
        command += '00'  # RESERVED
        command += '00'  # for STOP
        command += get_azimuth(parameters.get('sp_azimuth', 90))  # add azimuth
        command += '00' * 42  # RESERVED 42 bytes
        command += get_coordinates(parameters.get('sp_x', 59.97652),
                                   parameters.get('sp_y', 30.32138))  # add latitude and longitude in Double LE
        command += get_height(parameters.get('sp_height', 500))  # add height in float LE
        command += get_radius(parameters.get('sp_radius', 300))  # add circle radius in float LE
        command += get_speed(parameters.get('sp_speed', 20))  # add drone speed in float LE
        command += get_hex_from_ip_or_mask(parameters.get('sp_ip', '192.168.101.200'))  # not needed for circle IP
        command += '00' * 29  # RESERVED 29 bytes
        command += get_time()  # not needed
        command += get_time_synchro_interval()  # not needed
        command += '00' * 5  # not needed timing source conf
        command += get_hex_from_ip_or_mask(parameters.get('sp_mask', '255.255.255.0'))  # not needed MASK
        command += '00'  # memory last state
        command += '00'  # disable CA code noise
        command += '00' * 116  # RESERVED 116 bytes
        command_sum = get_sum(command)  # calculate command sum
        command += command_sum  # last byte of command sum
        command += 'edaa'  # end frame
    else:
        return False
    return command


def main():
    x = 59.97652
    y = 30.32138
    height = 500
    radius = 300
    speed = 20
    power = 44
    azimuth = 90
    mode = ['jamming', 'disperse', 'circle_pars', 'start_circle', 'stop']
    print(f'{'-' * 40}')
    print(f'Генерируем команду для передачи параметров режима КУПОЛ')
    print(f'{'-' * 40}')
    print(f'| Режим КУПОЛ с параметрами:'.ljust(40))
    print(f'| - Мощность: {power} {'дБм'.ljust(40)}')
    print(f'| - Координаты: {x}, {y}')
    print(f'| - Радиус: {radius} м')
    print(f'| - Высота: {height} м')
    print(f'| - Скорость: {speed} м/с')
    print(f'{'-' * 40}')
    print(f'{'Тестовая строка:'.ljust(23)} {test_circle_config_command}')
    command_for_circle_pars = generate_command(sp_mode=mode[2],
                                               sp_power=power,
                                               sp_x=x,
                                               sp_y=y,
                                               sp_height=height,
                                               sp_radius=radius,
                                               sp_speed=speed)
    if command_for_circle_pars:
        print(f'{'Сгенерированная строка:'.ljust(23)} {command_for_circle_pars}')
        if test_circle_config_command == command_for_circle_pars:
            print('Команды совпадают!')
        else:
            print('ОШИБКА!! Команды НЕ СОВПАДАЮТ')
    else:
        print("!!! Ошибка при генерации команды")
    print(f'{'-' * 40}')
    print(f'Генерируем команду для включения режима КУПОЛ')
    print(f'{'-' * 40}')
    print(f'{'Тестовая строка:'.ljust(23)} {test_start_circle_command}')
    command_for_start_circle = generate_command(sp_mode=mode[3],
                                                sp_power=power,
                                                sp_x=x,
                                                sp_y=y,
                                                sp_height=height,
                                                sp_radius=radius,
                                                sp_speed=speed)
    if command_for_start_circle:
        print(f'{'Сгенерированная строка:'.ljust(23)} {command_for_start_circle}')
        if test_start_circle_command == command_for_start_circle:
            print('Команды совпадают!')
        else:
            print('ОШИБКА!! Команды НЕ СОВПАДАЮТ')
    else:
        print("!!! Ошибка при генерации команды")
    print(f'{'-' * 40}')
    print(f'Генерируем команду для включения режима ОТКЛОНЕНИЕ')
    print(f'{'-' * 40}')
    print(f'| Режим ОТКЛОНЕНИЕ с параметрами:'.ljust(40))
    print(f'| - Мощность: {power} {'дБм'.ljust(40)}')
    print(f'| - Угол: {azimuth} гр.')
    print(f'{'-' * 40}')
    print(f'{'Тестовая строка:'.ljust(23)} {test_start_disperse_command}')
    command_for_start_disperse = generate_command(sp_mode=mode[1],
                                                  sp_power=power,
                                                  sp_azimuth=azimuth)
    if command_for_start_disperse:
        print(f'{'Сгенерированная строка:'.ljust(23)} {command_for_start_disperse}')
        if test_start_disperse_command == command_for_start_disperse:
            print('Команды совпадают!')
        else:
            print('ОШИБКА!! Команды НЕ СОВПАДАЮТ')
    else:
        print("!!! Ошибка при генерации команды")
    print(f'{'-' * 40}')
    print(f'Генерируем команду для включения режима ПОМЕХИ')
    print(f'{'-' * 40}')
    print(f'| Режим ПОМЕХИ с параметрами:'.ljust(40))
    print(f'| - Мощность: {power} {'дБм'.ljust(40)}')
    print(f'{'-' * 40}')
    print(f'{'Тестовая строка:'.ljust(23)} {test_start_jamming_command}')
    command_for_start_jamming = generate_command(sp_mode=mode[0],
                                                  sp_power=power)
    if command_for_start_jamming:
        print(f'{'Сгенерированная строка:'.ljust(23)} {command_for_start_jamming}')
        if test_start_jamming_command == command_for_start_jamming:
            print('Команды совпадают!')
        else:
            print('ОШИБКА!! Команды НЕ СОВПАДАЮТ')
    else:
        print("!!! Ошибка при генерации команды")
    print(f'{'-' * 40}')
    print(f'Генерируем команду для ВЫКЛЮЧЕНИЯ любого режима')
    print(f'{'-' * 40}')
    print(f'| Режим ВЫКЛЮЧЕНИЯ подавления:'.ljust(40))
    print(f'{'-' * 40}')
    print(f'{'Тестовая строка:'.ljust(23)} {test_stop_command}')
    command_for_stop = generate_command(sp_mode=mode[4],
                                                 sp_power=power)
    if command_for_stop:
        print(f'{'Сгенерированная строка:'.ljust(23)} {command_for_stop}')
        if test_stop_command == command_for_stop:
            print('Команды совпадают!')
        else:
            print('ОШИБКА!! Команды НЕ СОВПАДАЮТ')
    else:
        print("!!! Ошибка при генерации команды")
    print(f'{'-' * 40}')


if __name__ == "__main__":
    main()