import sys
import os
import re

def file_rename(path = ".", pattern = "Folder {{#}}"):
	targets = get_numbered_dirs(path)
	rename(targets, pattern)

def rename(targets, pattern):
	for target in targets:
		num = target["num"]
		path = target["path"]
		name = target["name"]
		new_name = re.sub("{{#}}", "{:02}".format(num), pattern)
		print("{0:02}: {1} --> {2}".format(num, name, new_name))
	
	proceed = input("Proceed with the rename? [y/n]: ")

	if proceed.lower() != 'y':
		print("Cancelling rename process.")
		return

	for target in targets:
		num = target["num"]
		path = target["path"]
		name = target["name"]
		new_name = re.sub("{{#}}", "{:02}".format(num), pattern)		
		os.rename(path + name, path + new_name)


def get_numbered_dirs(path = "."):
	assert len(path.strip()) > 0, "Path is blank"
	directory = os.scandir(path)

	prog = re.compile("\d+")
	folders = []
	for entry in directory:
		if entry.is_dir():
			filename_numbers = prog.findall(entry.name)
			if len(filename_numbers) == 0:
				continue
			num = int(filename_numbers.pop())
			folders.append({"num": num, "path": path if path.endswith("/") else path + "/", "name": entry.name})
	return sorted(folders, key=lambda folder: folder["num"])

def main():
	path = input("Enter a folder path: ")
	pattern = input("Enter a pattern for the new filename (use {{#}} to indicate where the volume number should go): ")

	file_rename(path, pattern)

if __name__ == "__main__":
	main()