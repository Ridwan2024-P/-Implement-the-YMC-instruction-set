import csv

def write_csv(data, filename="output.csv"):
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Address", "Assembly", "Registers", "Flags"])

        for row in data:
            writer.writerow(row)