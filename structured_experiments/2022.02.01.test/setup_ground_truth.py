import csv
import sys



def main():
	name_of_script = sys.argv[0] # should be setup_ground_truth.py
	kaggle_folder = sys.argv[1]
	with open(f'{kaggle_folder}/written_name_test.csv', mode='r') as csv_file:
	    csv_reader = csv.reader(csv_file, delimiter=',')
	    count = 0
	    for row in csv_reader:
	    	if count == 0: 
	    		count += 1
	    		continue
	    	elif count < 41:
	    		count += 1
	    		image_filename = row[0]
	    		ground_truth_text = row[1]
	    		ground_truth_filename = image_filename.replace("jpg", "gt.txt")
	    		with open(f'{kaggle_folder}/{ground_truth_filename}', mode='w') as ground_truth_file:
	    			ground_truth_file.write(ground_truth_text)

if __name__ == "__main__":
    main()
