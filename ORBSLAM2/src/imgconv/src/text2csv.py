import csv

def convert_text_to_csv(text_file_path, csv_file_path):
    with open(text_file_path, 'r') as text_file:
        lines = text_file.readlines()

    data = [line.strip().split(" ") for line in lines]
    
    with open(csv_file_path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(data)

# Example usage
text_file_path = '10.txt'
csv_file_path = 'deepv10.csv'
convert_text_to_csv(text_file_path, csv_file_path)

