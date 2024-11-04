import random

with open('esi.db', 'r+') as file:
    data = lines = [line.rstrip() for line in file]
    generated_esi = '00:' + ":".join([('0'+hex(random.randint(0,256))[2:])[-2:] for _ in range(9)])

    if generated_esi not in data:
        try:
            file.write(generated_esi + '\n')
            print(generated_esi)
        except:
            print('Error generating ESI')
    else:
        print('Generated ESI already in database. Run again!')