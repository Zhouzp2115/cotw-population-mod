import sys
from deca.file import ArchiveFile
from deca.ff_adf import Adf

class FakeVfs:
    def hash_string_match(self, hash32=None, hash48=None, hash64=None):
        return []

    def lookup_equipment_from_hash(self, name_hash):
        return None

def save_file(fname, data_bytes):
    with open(fname, "wb") as file:
        file.write(data_bytes)
        file.close()

in_file = sys.argv[1]

obj = Adf()
with ArchiveFile(open(in_file, 'rb')) as f:
    obj.deserialize(f)

concent = obj.dump_to_string(FakeVfs())
save_file(in_file+".txt", bytearray(concent, 'utf-8'))



