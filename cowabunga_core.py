import os
import struct

KEYS = {
    "cowabunga": 0x3F04B286,
    "atari": 0x2EEA4C8B,
    "atari-dlc1": 0x07853295,
    "atari-dlc2": 0x3AA19D18,
    "atari-dlc3": 0xD22D66C5,
    "making-karateka": 0x920DEA25,
    "garbage-pail-kids": 0xAA31713C,
    "jeff-minter": 0x34A4C18E,
    "blizzard-arcade": 0x93C8C18A,
    "mighty-morphin": 0xFA5E893B,
    "yu-gi-oh": 0x55D7F83B,
    "mortal-kombat-lc": 0x41D3AAA6,
    "golden-tee": 0x2E8D9A77,
    "rayman30th": 0x64DA7B23,
}

def rotate_left(n, d):
    return ((n << d) & 0xFFFFFFFF) | (n >> (32 - d))

def get_key(sum_val, game_key):
    temp1 = (rotate_left(sum_val, 15) * 0x1B873593 & 0xFFFFFFFF) ^ game_key
    temp2 = ((rotate_left(temp1, 13) * 5 & 0xFFFFFFFF) - 0x19AB949C) & 0xFFFFFFFF
    temp3 = (temp2 ^ 0x40000) >> 16
    temp4 = ((temp2 ^ temp3) * 0x85EBCA6B) & 0xFFFFFFFF
    temp5 = ((temp4 ^ (temp4 >> 13)) * 0xC2B2AE35) & 0xFFFFFFFF
    return (temp5 ^ (temp5 >> 16)) & 0xFFFFFFFF

def decrypt_block(block, offset_in_file, game_key):
    sum_val = (offset_in_file * 0xCC9E2D51) & 0xFFFFFFFF
    key = get_key(((offset_in_file & 0xFFFFFFFC) * 0xCC9E2D51) & 0xFFFFFFFF, game_key)
    
    decrypted = bytearray(block)
    for index in range(len(decrypted)):
        iter_bits = ((offset_in_file + index) & 3) << 3
        decrypted[index] ^= (key >> iter_bits) & 0xFF
        
        sum_val = (sum_val - 0x3361D2AF) & 0xFFFFFFFF
        if iter_bits == 24:
            key = get_key(sum_val, game_key)
            
    return decrypted

def is_valid_zip(file_path):
    try:
        with open(file_path, 'rb') as f:
            header = f.read(2)
            return header == b'PK'
    except Exception:
        return False

def process_file(input_path, output_path, game_key, progress_callback=None):
    file_size = os.path.getsize(input_path)
    block_size = 0x10000
    
    with open(input_path, 'rb') as f_in, open(output_path, 'wb') as f_out:
        processed = 0
        while True:
            buffer = f_in.read(block_size)
            if not buffer:
                break
            
            decrypted = decrypt_block(buffer, processed, game_key)
            f_out.write(decrypted)
            
            processed += len(buffer)
            if progress_callback:
                progress_callback(processed / file_size)

    if output_path.lower().endswith('.zip'):
        if not is_valid_zip(output_path):
            return False, "Not a valid ZIP file"
            
    return True, None
