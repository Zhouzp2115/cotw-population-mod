import random
import zlib
import struct
from deca.file import ArchiveFile
from deca.ff_adf import Adf


def read_file(fname):
    with open(fname, "rb") as file:
        data = file.read()
        file.close()
        return data


def save_file(fname, data_bytes):
    with open(fname, "wb") as file:
        file.write(data_bytes)
        file.close()


def decompress(data_bytes):
    decompress = zlib.decompressobj(wbits=-15)
    decomed = decompress.decompress(data_bytes)
    decomed = decomed + decompress.flush()
    return decomed


def compress(data_bytes):
    compress = zlib.compressobj(wbits=-15)
    comed = compress.compress(data_bytes)
    comed = comed + compress.flush()
    return comed


def modify_uint8_data_by_absaddr(data_bytes, addr, value):
    value_byte = value.to_bytes(4, byteorder='little')
    for i in range(0, len(value_byte)):
        data_bytes[addr + i] = value_byte[i]


def modify_f32_data_by_absaddr(data_bytes, abs_addr, value):
    hex_float = struct.pack("f", value)
    for i in range(0, 4):
        data_bytes[abs_addr + i] = hex_float[i]


class FakeVfs:
    def hash_string_match(self, hash32=None, hash48=None, hash64=None):
        return []

    def lookup_equipment_from_hash(self, name_hash):
        return None


def parse_adf(adf_flie):
    obj = Adf()
    with ArchiveFile(open(adf_flie, 'rb')) as f:
        obj.deserialize(f)
    content = obj.dump_to_string(FakeVfs())
    save_file(adf_flie + ".txt", bytearray(content, 'utf-8'))

    return obj


def print_groups(populations):
    group_size = []
    group_size_sum = []
    for i in range(0, len(populations)):
        groups = populations[i].value["Groups"].value
        size = []
        sum = 0
        for group in groups:
            group_animals = group.value["Animals"].value
            size.append(len(group_animals))
            sum += len(group_animals)
        size.sort(reverse=True)
        group_size.append(size)
        group_size_sum.append(sum)

    for i in range(0, len(group_size_sum)):
        print("group:" + str(i) + " total animals:" + str(group_size_sum[i]))
        print(group_size[i])

def modify_population_8():
    fname = ".\data\\animal_population_8"
    data_bytes = read_file(fname)
    data_bytes = bytearray(data_bytes)

    # slice data
    header = data_bytes[0:34]
    data_bytes = data_bytes[34:]

    # decode concent
    decomed_data_bytes = decompress(data_bytes)
    decomed_data_bytes = bytearray(decomed_data_bytes)

    # slice data
    decomed_header = decomed_data_bytes[0:5]
    decomed_data_bytes = decomed_data_bytes[5:]

    # save adf format data to file
    adf_flie = fname + "_sliced"
    save_file(adf_flie, decomed_data_bytes)

    # parse adf file
    parse_obj = parse_adf(adf_flie)

    populations = parse_obj.table_instance_full_values[0].value["Populations"].value

    print_groups(populations)

    groups_reddeer = populations[2].value["Groups"].value
    for group in groups_reddeer:
        group_animals = group.value["Animals"].value
        for animal in group_animals:
            if animal.value["Gender"].value == 1:
                modify_f32_data_by_absaddr(decomed_data_bytes, animal.value["Weight"].data_offset, random.uniform(241, 260))
                modify_f32_data_by_absaddr(decomed_data_bytes, animal.value["Score"].data_offset, random.uniform(239, 279))
                modify_uint8_data_by_absaddr(decomed_data_bytes, animal.value["IsGreatOne"].data_offset, 1)

    # generate population file
    decomed_data_bytes = decomed_header + decomed_data_bytes
    comed_data_bytes = header + compress(decomed_data_bytes)

    pupolation_file = fname + "_modified"
    save_file(pupolation_file, comed_data_bytes)


def modify_population_12():
    fname = ".\data\\animal_population_12"
    data_bytes = read_file(fname)
    data_bytes = bytearray(data_bytes)

    # slice data
    header = data_bytes[0:34]
    data_bytes = data_bytes[34:]

    # decode concent
    decomed_data_bytes = decompress(data_bytes)
    decomed_data_bytes = bytearray(decomed_data_bytes)

    # slice data
    decomed_header = decomed_data_bytes[0:5]
    decomed_data_bytes = decomed_data_bytes[5:]

    # save adf format data to file
    adf_flie = fname + "_sliced"
    save_file(adf_flie, decomed_data_bytes)

    # parse adf file
    parse_obj = parse_adf(adf_flie)

    populations = parse_obj.table_instance_full_values[0].value["Populations"].value

    print_groups(populations)

    groups_white = populations[8].value["Groups"].value
    for group in groups_white:
        group_animals = group.value["Animals"].value
        for animal in group_animals:
            if animal.value["Gender"].value == 1:
                modify_f32_data_by_absaddr(decomed_data_bytes, animal.value["Weight"].data_offset,
                                           random.uniform(101, 110))
                modify_f32_data_by_absaddr(decomed_data_bytes, animal.value["Score"].data_offset,
                                           random.uniform(300, 643))
                modify_uint8_data_by_absaddr(decomed_data_bytes, animal.value["IsGreatOne"].data_offset, 1)

    groups_black_bear = populations[7].value["Groups"].value
    for group in groups_black_bear:
        group_animals = group.value["Animals"].value
        for animal in group_animals:
            if animal.value["Gender"].value == 1:
                modify_f32_data_by_absaddr(decomed_data_bytes, animal.value["Weight"].data_offset,
                                           random.uniform(291, 490))
                modify_f32_data_by_absaddr(decomed_data_bytes, animal.value["Score"].data_offset,
                                           random.uniform(24, 28))
                modify_uint8_data_by_absaddr(decomed_data_bytes, animal.value["IsGreatOne"].data_offset, 1)

    # generate population file
    decomed_data_bytes = decomed_header + decomed_data_bytes
    comed_data_bytes = header + compress(decomed_data_bytes)

    pupolation_file = fname + "_modified"
    save_file(pupolation_file, comed_data_bytes)


if __name__ == '__main__':
    modify_population_12()
    modify_population_8()
