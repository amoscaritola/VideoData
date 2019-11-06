# https://github.com/amoscaritola

import os
import csv
import argparse

try:
	from pymediainfo import MediaInfo
except:
	print("The module pymediainfo can not be found. please run `pip3 install pymediainfo` and try again")
	exit(1)

def getListOfFiles(dirName):
	'''For the given path, get the List of all files in the directory tree'''
	listOfFile = os.listdir(dirName)
	allFiles = list()
	for entry in listOfFile:
		fullPath = os.path.join(dirName, entry)
		if os.path.isdir(fullPath):
			allFiles = allFiles + getListOfFiles(fullPath)
		else:
			allFiles.append(fullPath)
		print("Found {} files".format(len(allFiles)), end='\r')
	return allFiles

def getVidData(list_name):
	'''For list of files, returns list of lists containing filename and video resolution'''
	movie_list = [['Movie Title', 'Video Resolution']]
	count = 0
	for video in list_name:
		count += 1
		print("Checking file {}/{}".format(count, len(list_name)), end='\r')
		media_info = MediaInfo.parse(video)
		for track in media_info.tracks:
			if track.track_type == 'Video':
				atpos = video.rfind("/")
				resolution = "{}x{}".format(track.width, track.height)
				movie_list.append([video[atpos+1:], resolution])
	print("{} video(s) added to list".format(len(movie_list)))
	return movie_list
	
def write_to_csv(data):
	'''Write the data to a csv file'''
	csv_output = args.csv_path + "/" + "movie_list.csv"
	with open(csv_output, 'w') as csvFile:
		writer = csv.writer(csvFile)
		writer.writerows(data)	
	csvFile.close()
	
def main():
	if not args.csv_path:
		print("You must enter a destination for the csv output by using -o")
		exit()
	if args.dir_path:
		print("Creating list of files in directories and sub-directories")
		file_list = getListOfFiles(args.dir_path)
		print("Found {} files".format(len(file_list)))
		print("Checking the resolution of video files")
		data_list = getVidData(file_list)
		write_to_csv(data_list)
		print('Csv file created: {}/movie_list.csv'.format(args.csv_path))
	else:
		print("You must enter a directory to search using -i")

parser = argparse.ArgumentParser()
	
parser.add_argument('-i', '--input', dest='dir_path', 
	help="Enter the path of the directoty to search")

parser.add_argument('-o', '--output', dest='csv_path', 
	help="Enter the csv destination")

args = parser.parse_args()

if __name__ == '__main__':
	main()
