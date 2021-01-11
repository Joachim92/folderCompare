"""
    Compares contents of two folders and displays their differences with colors.

    Usage: python3 folderCompare.py <leftFolderPath> <rightFolderPath>

    Color meanings:
        yellow: file/folder only exist either in left or right folder
        red: file exists on both folders but it's contents are different
        black: files which are in both folders but couldn't be compared
"""
import filecmp
import argparse
from tkinter import ttk
import tkinter as tk
import re


def get_last_part_of_path(path: str) -> str:
    """Gets folder name from path, works in windows and linux"""
    multi_os_path = path.replace("\\", "/")
    return re.search("(?:[^/](?!/))+$", multi_os_path).group(0)


def insert_folder(tv, parent, side, left_path, right_path):
    fold_cmp = filecmp.dircmp(left_path, right_path, ignoreList)
    if side == "left":
        for f in fold_cmp.left_only:
            tv.insert(parent, "end", None, text=f, tags="lo")
    elif side == "right":
        for f in fold_cmp.right_only:
            tv.insert(parent, "end", None, text=f, tags="ro")
    for f in fold_cmp.diff_files:
        tv.insert(parent, "end", None, text=f, tags="dif")
    for f in fold_cmp.same_files:
        tv.insert(parent, "end", None, text=f, tags="same")
    for f in fold_cmp.funny_files:
        tv.insert(parent, "end", None, text=f, tags="funny")
    for subdir in fold_cmp.subdirs:
        fold = tv.insert(parent, "end", None, text=subdir, tags="sub")
        insert_folder(tv, fold, side, fold_cmp.left+"/"+subdir, fold_cmp.right+"/"+subdir)


def set_treeview_style(tv: ttk.Treeview, main_folder_name: str):
    """Sets Treeview cells background color based on the comparison"""
    # tv.tag_configure("same", background="#99B898", foreground="white")
    tv.tag_configure("lo", background="yellow", foreground="black")
    tv.tag_configure("ro", background="yellow", foreground="black")
    tv.tag_configure("dif", background="red", foreground="black")
    tv.tag_configure("funny", background="#2A363B", foreground="white")
    # tv.tag_configure("sub", background="#2A363B", foreground="white")
    tv.heading("#0", text=main_folder_name)
    style = ttk.Style()
    style.configure("Treeview.Heading", font=(None, 16))


# Start
parser = argparse.ArgumentParser(description="Compares the contents of two folders and displays their differences")
parser.add_argument("leftFolderPath", type=str)
parser.add_argument("rightFolderPath", type=str)
args = parser.parse_args()
leftFolderPath = args.leftFolderPath
rightFolderPath = args.rightFolderPath
ignoreList = [".DS_Store"]
hideList = None
folderComparison = filecmp.dircmp(leftFolderPath, rightFolderPath, ignoreList, hideList)

leftFolderName = get_last_part_of_path(leftFolderPath)
rightFolderName = get_last_part_of_path(rightFolderPath)

main_window = tk.Tk()
main_window.title("Folder Comparison")

tv1 = ttk.Treeview(selectmode="browse")
set_treeview_style(tv1, leftFolderName)
insert_folder(tv1, "", "left", leftFolderPath, rightFolderPath)
tv1.pack(side="left")

tv2 = ttk.Treeview(selectmode="browse")
set_treeview_style(tv2, rightFolderName)
insert_folder(tv2, "", "right", leftFolderPath, rightFolderPath)
tv2.pack(side="right")

t_view = ttk.Treeview(main_window)

main_window.mainloop()
