from hashlib import sha256
from os import linesep, path, walk

BUFFER_SIZE = 65536


def main() -> None:
    try:
        path1 = input(f'Path to file/folder 1: {linesep}')
        if not path1:
            print('Path 1 is empty!')
            return

        if not path.exists(path1):
            print('Path 1 does not exist!')
            return

        path2 = input(f'Path to file/folder 2: {linesep}')
        if not path2:
            print('Path 2 path is empty!')
            return

        if not path.exists(path1):
            print('Path 2 does not exist!')
            return

        if path1 == path2:
            print('Paths are the same!')
            return

        if path.isdir(path1) and not path.isdir(path2) or not path.isdir(path1) and path.isdir(path2):
            print('Different types of path, one is a file and the other is a folder!')
            return

        print_hash(path1, path2)

    except KeyboardInterrupt:
        print(f'{linesep}Operation interrupted by user!')
        return


def print_hash(path1: str, path2: str) -> None:
    if path.isfile(path1):
        hash_file1 = hash_file(path1)
        hash_file2 = hash_file(path2)
        if hash_file1 == hash_file2:
            print(f'{linesep}Hashes are the same!')
            return

        print(f'{linesep}Hashes are different!')
        print(f'\'{hash_file1}\' != \'{hash_file2}\'')
        return

    hash_path1 = create_folder_hash_map(path1)
    hash_path2 = create_folder_hash_map(path2)
    if hash_path1 == hash_path2:
        print(f'{linesep}Hashes are the same!')
        return

    hash1_keys = hash_path1.keys()
    hash2_keys = hash_path2.keys()

    missing_files = sorted(hash2_keys - hash1_keys, key=str.casefold)
    if missing_files:
        print(f'{linesep}Missing files in folder1: ')
        for file in missing_files:
            print(f'  \'{file}\'')

    missing_files = sorted(hash1_keys - hash2_keys, key=str.casefold)
    if missing_files:
        print(f'{linesep}Missing files in folder2: ')
        for file in missing_files:
            print(f'  \'{file}\'')

    common_files = sorted(hash1_keys & hash2_keys, key=str.casefold)
    print(f'{linesep}Different hashes: ')
    for file in common_files:
        hash1 = hash_path1[file]
        hash2 = hash_path2[file]
        if hash1 != hash2:
            print(f'  \'{file}\': \'{hash1}\' != \'{hash2}\'')


def create_folder_hash_map(folder_path: str) -> dict:
    hash_tree = {}
    for root, _, files in walk(folder_path):
        for file in files:
            file_path = path.join(root, file)
            rel_path = path.relpath(file_path, folder_path)
            hash_tree[rel_path] = hash_file(file_path)
    return hash_tree


def hash_file(file_path: str) -> str:
    hasher = sha256()
    with open(file_path, 'rb') as f:
        while True:
            data = f.read(BUFFER_SIZE)
            if not data:
                break
            hasher.update(data)
    return hasher.hexdigest()


if __name__ == '__main__':
    main()
