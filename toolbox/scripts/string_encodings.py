import sys
import hashlib
import base64
import binascii


def main():
    def output(title, value):
        print('==== {} ===='.format(title))
        print(value)
        print()

    string = sys.argv[1]
    string = string.encode('ascii', errors='ignore').decode('ascii')

    output('Input', '{} (length: {})'.format(string, len(string)))

    for descr, func in [
        ['MD5 (encoded)', to_md5],
        ['Hex (encoded)', to_hex],
        ['Base64 (encoded)', to_base64],
        ['Code points (encoded)', to_code_points],

        ['Hex (decoded)', from_hex],
        ['Base64 (decoded)', from_base64],
        ['Code points (decoded)', from_code_points],

    ]:
        try:
            output(descr, func(string))
        except ValueError:
            pass


def to_md5(string: str) -> str:
    return hashlib.md5(string.encode('ascii')).hexdigest()


def to_base64(string: str) -> str:
    return base64.b64encode(string.encode('ascii')).decode('ascii')


def from_base64(string: str) -> str:
    return base64.b64decode(string).decode('ascii')


def to_hex(string: str) -> str:
    return binascii.hexlify(string.encode('ascii')).decode('ascii')


def from_hex(string: str) -> str:
    return bytes.fromhex(string).decode('ascii')


def to_code_points(string: str) -> str:
    code_points = [str(ord(letter)) for letter in string]
    return ','.join(code_points)


def from_code_points(string: str) -> str:
    characters = [chr(int(code)) for code in string.split(',')]
    return ''.join(characters)


if __name__ == '__main__':
    main()
