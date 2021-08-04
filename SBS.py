from genericpath import isfile
import os
from pathlib import Path
import sys


import SBSSqlite


class CLFileReader:
    def __init__(self) -> None:
        args = sys.argv
        arg_len = len(args)
        if arg_len <= 1 or arg_len > 3:
            self._log("参数个数异常")
            sys.exit()

        self._file_names = []
        self._cur_index = 0

        if arg_len == 1:
            self._file_names.append(args[1])
            return

        if args[1] == '-d':
            self._dir_name=args[2]
            files = self._read_all_files(args[2])
            if files:
                self._file_names.extend(files)
            return

        self._log("参数异常")
        sys.exit()

    def _read_all_files(self, dir):
        if not os.path.isdir(dir):
            return None
        files = []
        for f in os.listdir(dir):
            is_file = isfile(os.path.join(dir, f))
            has_ext = True
            extension = Path(f).suffix
            if not extension:
                has_ext = False

            if is_file and has_ext:
                files.append(f)
        return files

    def _log(self, msg):
        print(msg)

    def has_next(self):
        return self._cur_index + 1 < len(self._file_names)

    def has_cur(self):
        return self._cur_valid()

    def _cur_valid(self):
        return self._cur_index < len(self._file_names)

    def move_next(self):
        if self.has_next():
            self._cur_index += 1

    def get_cur_bin(self):
        if self._cur_valid():
            name=self._file_names[self._cur_index]
            f = open(os.path.join(self._dir_name,name), "rb")
            return f.read()
        else:
            return None

    def get_cur_full_name(self):
        if self._cur_valid():
            return self._file_names[self._cur_index]
        else:
            return None

    def get_cur_create_date(self):
        #TODO: implement
        return None


def get_bin_data(reader: CLFileReader):
    data = dict()
    if not reader.has_cur():
        return None
    data["name"] = reader.get_cur_full_name()
    data["ext"] = Path(reader.get_cur_full_name()).suffix
    data["data"] = reader.get_cur_bin()
    data["create_date"] = reader.get_cur_create_date()
    return data


def main():
    reader = CLFileReader()
    sqlite = SBSSqlite.SBSSqlite()
    con = sqlite.get_sqlite_connection()

    while True:
        bin = get_bin_data(reader)
        if bin:
            sqlite.sqlite_insert_bin(con, bin)

        if not reader.has_next():
            break
        else:
            reader.move_next()

    con.close()


if __name__ == '__main__':
    main()