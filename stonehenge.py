from flask import Flask, render_template

app = Flask(__name__)

from shdecoders import *
from shdbops import *

import time


@app.errorhandler(500)
def page_not_found(error):
    print(error)
    return "500: " + str(error)


@app.route('/')
def display_index():
    posts = getlimitedposts(100)
    return render_template('show_posts.html', posts=posts)


@app.route('/solved')
def display_solved():
    posts = getsolvedposts()
    return render_template('show_posts.html', posts=posts)


@app.route('/unsolved')
def display_unsolved():
    posts = getunsolvedposts()
    return render_template('show_posts.html', posts=posts)


@app.route('/post/<int:post_id>')
@app.route('/id/<int:post_id>')
def show_id(post_id):
    post = getbyid(post_id)
    return display_post(post)


@app.route('/post/<string:post_shortcode>')
@app.route('/shortcode/<string:post_shortcode>')
def show_shortcode(post_shortcode):
    post = getbyshortcode(post_shortcode)
    return display_post(post)


@app.route('/title/<string:post_title>')
def show_title(post_title):
    post = getbytitle(post_title)
    return display_post(post)


def display_post(post):
    post.link = "" if not (hasattr(post, 'link')) else post.link
    post.shortcode = get_shortcode(post.link) if not (hasattr(post, 'shortcode')) else post.shortcode
    post.length = get_length(post.content) if not (hasattr(post, 'length')) else post.length
    post.md5 = get_md5(post.content) if not (hasattr(post, 'md5')) else post.md5
    post.soulsphere = get_soulsphere(post.shortcode)
    post.redditwiki = get_redditwiki(post.title)
    post.unhex = unhex(post.content)
    post.unb64 = unb64(post.unhex)
    post.unb64_utf8 = unb64codec(post.unb64, 'utf-8')
    # post.unb64_utf8_ascii = utf2ascii(post.unb64_utf8)
    post.unb64_utf8_unhex = unhex(post.unb64_utf8)
    post.b64 = b64(post.content)
    md5a858 = "34a14a42e98ff96095af56604e290cae"
    md5a858des3 = des3decrypt(post.content, md5a858)
    md5a858des3cbc = des3decryptcbc(post.content, md5a858, "0000000000000000")
    post.md5a858des3 = md5a858des3
    post.md5a858des3_utf8 = unb64codec(md5a858des3, 'utf-8')
    try:
        post.md5a858des3cbc = str(md5a858des3cbc, encoding='utf-8', errors='replace')
    except:
        post.md5a858des3cbc = md5a858des3cbc
        pass
    recursiveapproach = find_approach(post.content)
    recursivekeys = find_keys(post.content, recursiveapproach)
    recursivesolution = solve(post.content, recursiveapproach)
    post.recursiveapproach = str(recursiveapproach if solvedapproach(recursiveapproach) else [])
    post.recursivekeys = str(recursivekeys)
    post.recursivesolution = str(recursivesolution, encoding='utf-8', errors='replace')
    return render_template('show_one_post.html', post=post)


if __name__ == '__main__':
    app.run(host='0.0.0.0')


def populate_solutions(auto=False):
    posts = getallposts()
    total = len(posts)
    cur = 0
    for post in posts:
        cur += 1
        print(str(cur) + "/" + str(total) + " ####################### " + str(
            post.id) + " " + post.title + " " + post.shortcode + " #######################")
        approach = find_approach(post.content)
        solution = solve(post.content, approach)
        key = find_keys(post.content, approach)
        newkey = '' if len(key) == 0 else key[0].decode('utf-8')
        newauto_approach = ','.join(approach) if solvedapproach(approach) else ''
        newauto_solution = solution.decode('utf-8')
        if newkey != post.key or newauto_approach != post.auto_approach or newauto_solution != post.auto_solution:
            print("New solution found for " + post.title + " " + post.shortcode)
            print("Old Approach: " + str(post.auto_approach))
            print("New Approach: " + str(newauto_approach))
            print("Old Key: " + str(post.key))
            print("New Key: " + str(newkey))
            try:
                print("Old Solution: \n" + str(post.auto_solution))
            except:
                print("Old Solution: cannot print")
                pass
            try:
                print("New Solution: \n" + str(newauto_solution))
            except:
                print("New Solution: cannot print")
                pass
            answer = 'yes' if auto else input("Do you want to accept this change? (Type 'yes' to accept): ")
            if answer == 'yes':
                print("Saving for database commit.")
                post.key = newkey
                post.auto_approach = newauto_approach
                post.auto_solution = newauto_solution
                session.commit()
            else:
                print("Discarding change. Will not be saved in database commit.")
    session.commit()
    return True


# bruteforce
def bruteforce(startkey=0, endkey=340282366920938463463374607431768211455, keylength=32, auto=False):
    config.bf = True
    starttime = time.time()
    posts = getunsolvedposts()
    total = len(posts)
    keynum = startkey
    if keylength % 2 != 0:
        keylength += 1
    while keynum <= endkey:
        keytime = time.time()
        ununpaddedkey = hex(keynum)[2:].encode('utf-8')
        if len(ununpaddedkey) % 2 != 0:
            ununpaddedkey = b'0' + ununpaddedkey
        unpaddedkey = binascii.unhexlify(ununpaddedkey)
        mykey = bytes(int(keylength / 2) - len(unpaddedkey)) + unpaddedkey
        print("!!!!!!!!!!!!!!!! Elapsed Time: " + str((time.time() - starttime) / 60) + " min")
        print("!!!!!!!!!!!!!!!! Starting key: " + binascii.hexlify(mykey).decode('utf-8') + " !!!!!!!!!!!!!!!!")
        cur = 0
        for post in posts:
            config.keylist = [mykey]
            # print(str(config.keylist))
            cur += 1
            # print(str(cur)+"/"+str(total)+" ####################### "+str(post.id)+" "+post.title+" "+post.shortcode+" #######################")
            if cur % 1000 == 0:
                print("################ Post " + str(cur) + "/" + str(total) + " at " + str(
                    (time.time() - starttime) / 60) + " min")
            approach = find_approach(post.content)
            solution = solve(post.content, approach)
            key = find_keys(post.content, approach)
            newkey = '' if len(key) == 0 else key[0].decode('utf-8')
            newauto_approach = ','.join(approach) if solvedapproach(approach) else ''
            newauto_solution = solution.decode('utf-8')
            if newkey != post.key or newauto_approach != post.auto_approach or newauto_solution != post.auto_solution:
                print("New solution found for " + post.title + " " + post.shortcode)
                print("Old Approach: " + str(post.auto_approach))
                print("New Approach: " + str(newauto_approach))
                print("Old Key: " + str(post.key))
                print("New Key: " + str(newkey))
                try:
                    print("Old Solution: \n" + str(post.auto_solution))
                except ValueError:
                    print("Old Solution: cannot print")
                    pass
                try:
                    print("New Solution: \n" + str(newauto_solution))
                except:
                    print("New Solution: cannot print")
                    pass
                answer = 'yes' if auto else input("Do you want to accept this change? (Type 'yes' to accept): ")
                if answer == 'yes':
                    print("Saving for database commit.")
                    post.key = newkey
                    post.auto_approach = newauto_approach
                    post.auto_solution = newauto_solution
                    session.commit()
                else:
                    print("Discarding change. Will not be saved in database commit.")
        session.commit()
        print("!!!!!!!!!!!!!!!! Time per post: " + str((time.time() - keytime) / total) + " sec")
        print("!!!!!!!!!!!!!!!! Time per key: " + str(
            ((time.time() - starttime) / (keynum + 1 - startkey)) / 60) + " min")
        print("!!!!!!!!!!!!!!!! Ending key:   " + binascii.hexlify(mykey).decode('utf-8') + " !!!!!!!!!!!!!!!!")
        keynum += 1
    return True
