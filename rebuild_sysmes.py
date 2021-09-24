# the original sysmes here
sysmes = open('SYSMES_TEXT.DAT', 'rb')
old_data = sysmes.read()

# the translated texts here
translation = open('sysmes_text.txt', 'rb')
translations = translation.read().splitlines()

# output of new sysmes here
new_sysmes = open('SYSMES_TEXT_NEW.DAT', 'wb')

count_offset = '0x4'
int_pos = int(count_offset, 16)
string_count = int.from_bytes(old_data[int_pos:int_pos + 4], byteorder='little')

if len(translations) != string_count:
    raise SystemExit('Wrong number of strings in translation file!')

header_offset = '0x18'
first_position = int(header_offset, 16)

# header offset + string_count * 8
strings_position = first_position + string_count * 8
# TODO calculate this offset
footer_offset = '0x184DA'

# prepare header and footer
# we will prepend our new data with this
header_data = old_data[0:int(header_offset, 16)]
# we will append our new data with this
footer_data = old_data[int(footer_offset, 16):len(old_data)]

# write header
new_sysmes.write(header_data)
# write string positions
pos = first_position
i = 0
while pos < first_position + string_count * 8:
    new_sysmes.write(strings_position.to_bytes(8, byteorder='little'))
    pos += 8
    strings_position += len(translations[i]) + 1    # +1 because there will be a 00 byte after each string
    i += 1

# write strings
for t in translations:
    new_sysmes.write(t)
    new_sysmes.write(bytes([0x00]))

# write footer
new_sysmes.write(footer_data)

sysmes.close()
translation.close()
new_sysmes.close()
