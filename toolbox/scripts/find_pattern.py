import sys

patterns = [
    [b'Flag', '"Flag"'],
    [b'flag', '"flag"'],
    [b'galF', '"Flag" spelled backwards'],
    [b'galf', '"flag" spelled backwards'],
    [b'RmxhZ', '"Flag..." in Base64'],
    [b'ZmxhZ', '"flag..." in Base64'],
    [b'466c6167', '"Flag" in Hex'],
    [b'466C6167', '"Flag" in Hex'],
    [b'666c6167', '"flag" in Hex'],
    [b'666C6167', '"flag" in Hex'],

    [b'Steg', '"Steg"'],
    [b'steg', '"steg"'],
    [b'U3RlZ', '"Steg..." in Base64'],
    [b'c3RlZ', '"steg..." in Base64'],
    [b'53746567', '"Steg..." in Hex'],
    [b'73746567', '"steg..." in Hex'],

    # [b'jpg', '"jpg"'],
    # [b'jpeg', '"jpeg"'],
    # [b'JPG', '"JPG"'],
    # [b'JPEG', '"JPEG"'],
    [b'\xff\xd8\xff', 'JPG Header'],
    # [b'\xff\xd9', 'JPG (end of file)'],

    # [b'gif', '"gif"'],
    # [b'GIF', '"GIF"'],
    [b'\x47\x49\x46\x38', 'GIF Header'],

    [b'\xa1\xb2\xc3\xd4', 'PCAP header'],
    [b'\xd4\xc3\xb2\xa1', 'PCAP header (reverse)'],
]


def main():
    def print_match(offset):
        print("{} ({}):".format(hex(offset), offset))
        print(blob[offset:offset + 50])
        print()

    with open(sys.argv[1], 'rb') as f:
        blob = f.read()
    for pattern, descr in patterns:
        offsets = []
        start = 0
        while True:
            index = blob.find(pattern, start)
            if index == -1:
                break
            offsets.append(index)
            start = index + 1

        if not offsets:
            continue

        print('\n==== Matches for {} ({}) ===='.format(descr, pattern))
        for offset in offsets:
            print_match(offset)


if __name__ == '__main__':
    main()
