sysmes = open('SYSMES_TEXT.DAT', 'rb')

data = sysmes.read()

count_offset = '0x4'

int_pos = int(count_offset, 16)
string_count = int.from_bytes(data[int_pos:int_pos + 4], byteorder='little')

print('Found', string_count, 'strings')

header_offset = '0x18'

# first we read the header with the string offsets
positions = []
first_position = int(header_offset, 16)
i = first_position
while i < first_position + string_count * 8:
    positions.append(int.from_bytes(data[i:i + 8], byteorder='little'))
    i += 8

# then we read the strings on those positions

output = open('sysmes_text.txt', 'w+', encoding="utf-8")

for position in positions:
    int_pos = position

    values = []
    texts = []

    value = data[int_pos]

    while value != 0:
        values.append(value)
        int_pos += 1
        value = data[int_pos]

    text = bytearray(values).decode('utf-8')
    texts.append(text)
    print(hex(position) + ': ' + text)
    output.write(text + "\n")


sysmes.close()
output.close()
