
import sys

def Open(file_name, mode):

    try:
        # encoding='utf-8'
        file = open(file_name, mode, encoding='utf-8')
    except IOError as e:
        print(f"ERORR: file '{file_name}' could not be opened in the '{mode}'!")
        print(f"Error details: {e}")
        return None
    else:
        print(f"File '{file_name}' successfully opened in the mode '{mode}'.")
        return file

file1_name = "TF26_1.txt"
file2_name = "TF26_2.txt"

print("A: Creating a file TF26_1.txt ")
file1_w = Open(file1_name, "w")

if file1_w:
    try:
        lines_to_write = [
            "Shall I compare thee to a summer’s day?",
            "Thou art more lovely and more temperate:",
            "Rough winds do shake the darling buds of May,",
            "And summer’s lease hath all too short a date:",
            "",
            "Sometime too hot the eye of heaven shines,",
            "And often is his gold complexion dimmed;",
            "And every fair from fair sometime declines,",
            "By chance or nature’s changing course untrimmed;",
            "",
            "But thy eternal summer shall not fade",
            "Nor lose possession of that fair thou ow’st;",
            "Nor shall Death brag thou wander’st in his shade,",
            "When in eternal lines to time thou grow’st:",
            "",
            "So long as men can breathe or eyes can see,",
            "So long lives this, and this gives life to thee."
        ]
        
        for line in lines_to_write:
            file1_w.write(line + "\n")
            
        print(f"Data successfully written to file {file1_name}.")
        
    except IOError as e:
        print(f"ERORR: writing to a file {file1_name}: {e}")
    finally:
        file1_w.close()
        print(f"File {file1_name} closed.")
else:
    print(f"ERORR: failed {file1_name}. Work stoped.")
    sys.exit()


print(f"\nB: Conversion from {file1_name} to {file2_name}")


file1_r = Open(file1_name, "r")
file2_w = None

if file1_r:
    try:
        file2_w = Open(file2_name, "w")
        
        if file2_w:
            print("Both files are open. Let's start the conversion...")
            for line in file1_r:
                lower_line = line.lower()
                file2_w.write(lower_line)
            
            print(f"Data successfully converted and written to {file2_name}.")
        else:
            print(f"ERORR: failed to open {file2_name} for the record. Stage B skasovan.")
            
    except IOError as e:
        print(f"ERROR: reading/writing {e}")
    finally:
        if file1_r:
            file1_r.close()
            print(f"File {file1_name} close.")
        if file2_w:
            file2_w.close()
            print(f"File {file2_name} close.")
else:
    print(f"ERORR: failed to open {file1_name} for reading. Stage B skasovaniye.")


print(f"\nStage C: Print the contents of the file {file2_name}")

file2_r = Open(file2_name, "r")

if file2_r:
    try:
        print(f"File {file2_name}:")
        print("---------------------------------")
        
        for line in file2_r:
            print(line, end='')
        print("\n---------------------------------")
        
    except IOError as e:
        print(f"ERORR: not read file {file2_name}: {e}")
    finally:
        file2_r.close()
        print(f"File {file2_name} closed.")
else:
    print(f"ERORR: failed to open {file2_name} for reading. Stage C cancelled.")