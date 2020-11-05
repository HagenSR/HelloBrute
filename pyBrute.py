import random
import sqlite3
import hashlib
import time

conn = sqlite3.connect('data.db')
cursor = conn.cursor()

Letters = ['H', 'E', 'L', 'O', 'W', 'R', 'D', ' ']
good = "HELLO WORLD"
run = 0


def percentLike(word):
    count = 0
    for letter in range(0, len(word) - 1):
        if good[letter] is word[letter]:
            count += 1
    return count / 11


def enterData(word, close):
    try:
        md5Hash = hashlib.md5()
        md5Hash.update(word.encode('utf-8'))
        hs = abs(int(md5Hash.hexdigest(), 16) % 9223372036854775807)

        cursor.execute('SELECT occurance FROM trys WHERE hash=?', (hs,))
        res = cursor.fetchone()
        if res is None:
            cursor.execute('INSERT INTO trys VALUES (?, ?, ?, ?)',(hs, word, 1, close))
        else:
            nim = res[0]
            nim += 1
            cursor.execute('UPDATE trys SET occurance = ? WHERE hash=?', (nim, hs))
        conn.commit()
    except Exception as e:
        print(str(e))

def insertStats(trys, strt):
    cursor.execute('SELECT run FROM stats ORDER BY run desc')
    res = cursor.fetchone()
    span = (time.time() - strt)
    if res is None:
        cursor.execute('INSERT INTO stats VALUES (?, ?, ?)',(1, trys, span))
    else:
        run = res[0]
        run += 1
        cursor.execute('INSERT INTO stats VALUES (?, ?, ?)',(run, trys, span))
    cursor.close();
    conn.commit();


if __name__ == "__main__":
    rtn = ""
    diction = {}
    run += 1
    strt = time.time()
    while rtn is not good:
        rtn = ""
        for num in range(len(good)):
            rnd = random.randint(0, 7)
            rtn += Letters[rnd]
        pcr = percentLike(rtn)
        enterData(rtn, pcr)
    print("DONE")
    insertStats(run, strt)
