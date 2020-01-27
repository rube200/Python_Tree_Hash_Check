import hashlib, os



def __SubFolder_Tree_Check(Folder1_Path, Folder2_Path, CheckSubFolders, MissingFiles, CheckedFolders):
	for file in os.listdir(Folder1_Path):
		file_Path1 = os.path.join(Folder1_Path, file)
		file_Path2 = os.path.join(Folder2_Path, file)


		if not os.path.isdir(file_Path1) or file in CheckedFolders:
			continue


		if file_Path2 in MissingFiles:
			continue


		if not os.path.isdir(file_Path2):
			MissingFiles.append(file_Path2 + " is a File AND " + file_Path1 + " is a Folder!!" )
			continue


		CheckedFolders.append(file_Path1)
		__Folder_Tree_Check(file_Path1, file_Path2, CheckSubFolders, MissingFiles, CheckedFolders)
	return


def __Folder_Tree_Check(Folder1_Path, Folder2_Path, CheckSubFolders, MissingFiles = [], CheckedFolders = []):
	Folder1_Files = os.listdir(Folder1_Path)
	Folder2_Files = os.listdir(Folder2_Path)


	MissingFiles += [os.path.join(Folder2_Path, f) for f in Folder1_Files if not f in Folder2_Files and os.path.join(Folder2_Path, f) not in MissingFiles]


	if CheckSubFolders:
		__SubFolder_Tree_Check(Folder1_Path, Folder2_Path, CheckSubFolders, MissingFiles, CheckedFolders)
	return


def Folder_Tree_Check(Folder1_Path, Folder2_Path, CheckSubFolders = True):
	MissingFiles = []
	CheckedFolders = []


	__Folder_Tree_Check(Folder2_Path, Folder1_Path, CheckSubFolders, MissingFiles, CheckedFolders)
	__Folder_Tree_Check(Folder1_Path, Folder2_Path, CheckSubFolders, MissingFiles, CheckedFolders)


	if len(MissingFiles) != 0:
		print("\tFolder Tree: Failed")
		print("\tContent not found:")
		for file in MissingFiles:
			print("\t\t" + file)
	else:
		print("\tFolder Tree: OK")
	return


#os.walk()
def __Folder_Hash_Check(Folder1_Name, Folder2_Name, CheckSubFolders = True, HashFails = [], Current_Path = ""):
	Folder1_Path = os.path.join(Folder1_Name, Current_Path)
	for file in os.listdir(Folder1_Path):
		file_BasePath = os.path.join(Current_Path, file)
		file_Path1 = os.path.join(Folder1_Name, file_BasePath)
		file_Path2 = os.path.join(Folder2_Name, file_BasePath)
		

		if os.path.isdir(file_Path1):
			if CheckSubFolders:
				__Folder_Hash_Check(Folder1_Name, Folder2_Name, CheckSubFolders, HashFails, file_BasePath)
			continue


		if not os.path.exists(file_Path2) or os.path.isdir(file_Path2):
			continue



		Hash = hashlib.sha1()
		Original_File = open(file_Path1, "rb")
		Original_Content = Original_File.read()

		Hash.update(Original_Content)
		Original_File.close()
		Original_Hash = Hash.hexdigest()
		
		

		Hash = hashlib.sha1()
		Modded_File = open(file_Path2, "rb")
		Modded_Content = Modded_File.read()
		
		Hash.update(Modded_Content)
		Modded_File.close()
		Modded_Hash = Hash.hexdigest()
		


		if Original_Hash != Modded_Hash:
			HashFails.append(file_BasePath + " > (" + Folder1_Name + ") " + Original_Hash + " || (" + Folder2_Name + ") " + Modded_Hash)
			continue
	return


def Folder_Hash_Check(Folder1_Path, Folder2_Path, CheckSubFolders = True):
	HashFails = []


	__Folder_Hash_Check(Folder1_Path, Folder2_Path, CheckSubFolders, HashFails)


	if len(HashFails) != 0:
		print("\tHash: Failed")
		print("\tFiles:")
		for file in HashFails:
			print("\t\t" + file)
	else:
		print("\tHash: OK")
	return




if __name__ == '__main__':
	Folder1_Name = "Folder1"
	Folder2_Name = "Folder2"


	print("\n\n")
	Folder_Tree_Check(Folder1_Name, Folder2_Name, True)


	print("\n\n")
	Folder_Hash_Check(Folder1_Name, Folder2_Name, True)