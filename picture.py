import numpy as np
from PIL import Image
import os

# Constants, parameters of LCD
pages = 8
column_adr = 128  # Summa of all addresses on all crystals

# Print out all pictures in same folder
actual_files = []
print('\nPictures:')
for root, dirs, files in os.walk("."):
    for filename in files:
        if filename[-3:] == 'png' or filename[-3:] == 'jpg':
            actual_files.append(filename)
            print(filename)

frames = {}
while True:
    print(f'Already chose: {[i for i in list(frames.keys())]}')
    file_name = input('\nTo convert enter "STOP"\nEnter picture name:')
    if file_name == 'STOP':
        break
    try:
        image_frame = Image.open(file_name).convert('1')  # Convert to black and white
        frames[file_name] = image_frame
        continue
    except FileNotFoundError:
        print('\nThere is no such file in folder, try again\n'
              'Actual files:')
    except AttributeError:
        print('Blank line!')
    finally:
        [print(i) for i in actual_files]

# Do multiple convert
answer = ''
for file_name, image_frame in list(frames.items()):
    # Check size of picture
    w, h = image_frame.size
    if w != column_adr or h != pages * 8:
        quit('Wrong image size')

    np_array = np.asarray(image_frame)

    # Change array to byte type
    result = np.zeros((pages, column_adr))
    count = 0
    answer += f'static uint8_t {file_name[:-4]}[1024] = ' + '{\n'
    for i in range(pages):
        for j in range(column_adr):
            for k in range(8):
                result[i][j] += np_array[k + i * 8][j] * 2 ** k
            # Invert number: before black=0, now black=1
            result[i][j] = 255 - result[i][j]
            # Add new symbols to final string
            count += 1
            if count % 32 == 0:  # To better readable use \n
                answer += f'{int(result[i][j])},\n'
            else:
                answer += f'{int(result[i][j])}, '

    # Final formatting
    answer = answer[:-2]
    answer += '};\n\n'

with open('result.txt', 'w') as new_file:
    new_file.write(answer)
