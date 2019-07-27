import sys


class PcapCarver:
    MAGIC_NUMBER = b'\xa1\xb2\xc3\xd4'
    MAGIC_NUMBER_SWAPPED = b'\xd4\xc3\xb2\xa1'

    PCAP_GLOBAL_HEADER_LEN = 24
    PCAP_PACKET_HEADER_LEN = 16

    OFFSET_TS_SEC = 0x0
    OFFSET_TS_USEC = 0x4
    OFFSET_INCL_LEN = 0x8
    OFFSET_ORIG_LEN = 0x12

    def __init__(self, blob):
        offset_magic = blob.find(self.MAGIC_NUMBER)
        offset_magic_swapped = blob.find(self.MAGIC_NUMBER_SWAPPED)

        if offset_magic != -1:
            self.endianness = 'big'
            self.blob = blob[offset_magic:]
        elif offset_magic_swapped != -1:
            self.endianness = 'little'
            self.blob = blob[offset_magic_swapped:]

    def get_file(self):
        """Returns the first pcap file found."""
        offset = self.PCAP_GLOBAL_HEADER_LEN
        while self.is_valid_packet_header(offset):
            packet_length = self.read_uint32(offset + self.OFFSET_INCL_LEN)
            offset += self.PCAP_PACKET_HEADER_LEN + packet_length
        return self.blob[:offset]

    def is_valid_packet_header(self, offset):
        """Heuristic for determining whether there is a valid pcap packet header at this offset."""
        ts_sec = self.read_uint32(offset + self.OFFSET_TS_SEC)
        ts_usec = self.read_uint32(offset + self.OFFSET_TS_USEC)
        incl_len = self.read_uint32(offset + self.OFFSET_INCL_LEN)
        orig_len = self.read_uint32(offset + self.OFFSET_ORIG_LEN)
        constraints = [
            1400000000 < ts_sec < 1600000000,  # between July 2017 and Sep 2020
            ts_usec < 1000000,  # must be less than one second
            incl_len <= orig_len  # captured length must not exceed original length
        ]
        likely_valid = sum([1 for c in constraints if not c]) == 0
        return likely_valid

    def read_uint32(self, offset):
        uint32 = self.blob[offset: offset + 4]
        return int.from_bytes(uint32, byteorder=self.endianness)


if __name__ == '__main__':
    fs = sys.argv[1]
    with open(fs, 'rb') as f:
        blob = f.read()

    carver = PcapCarver(blob)
    file = carver.get_file()
    with open('file.pcap', 'wb') as f:
        f.write(file)
        f.close()
