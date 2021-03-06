#!/usr/bin/env python
import hashlib
import sys
import inspect

try:
    import requests
except ModuleNotFoundError:
    print("###  pip install requests  ###")
    raise


def print_function_name():
    print("-->", inspect.stack()[1][3])


def lookup_pwned_api(pwd):
    """Returns hash and number of times password was seen in pwned database.

    Args:
        pwd: password to check

    Returns:
        A (sha1, count) tuple where sha1 is SHA-1 hash of pwd and count is number
        of times the password was seen in the pwned database.  count equal zero
        indicates that password has not been found.

    Raises:
        RuntimeError: if there was an error trying to fetch data from pwned
            database.
        UnicodeError: if there was an error UTF_encoding the password.
    """
    sha1pwd = hashlib.sha1(pwd.encode('utf-8')).hexdigest().upper()
    head, tail = sha1pwd[:5], sha1pwd[5:]
    print(f"Checking password: {pwd} {head}")
    url = 'https://api.pwnedpasswords.com/range/' + head
    print(f"URL: {url}")
    res = requests.get(url)
    if not res.ok:
        raise RuntimeError('Error fetching "{}": {}'.format(
            url, res.status_code))
    # count = occurences_count(res.text, tail)
    # count = occurences_count_2(res.text, tail)
    # count = occurences_count_3(res.text, tail)
    # count = occurences_count_4(res.text, tail)
    # count = occurences_count_5(res.text, tail)
    count = occurences_count_6(res.text, tail)
    return sha1pwd, count


def occurences_count(text, tail):
    print_function_name()

    hashes = (line.split(':') for line in text.splitlines())
    count = next((int(count) for t, count in hashes if t == tail), 0)

    return count


def occurences_count_2(text, tail):
    print_function_name()

    lines = text.splitlines()
    hashes = []         # JR start with empty list
    for line in lines:
        hashes.append(line.split(':'))

    matches_generator = (int(count) for t, count in hashes if t == tail)
    count = next(matches_generator, 0)

    return count


def occurences_count_3(text, tail):
    print_function_name()
    hashes_generator = (line.split(':') for line in text.splitlines())
    hashes = list(hashes_generator)

    print(f"matching tails count: {len(hashes)}")

    matches_generator = (count for t, count in hashes if t == tail)
    # only expecting one result, so only one call to next()
    count = next(matches_generator, 0)

    return count


def occurences_count_4(text, tail):
    print_function_name()
    hashes = [line.split(':') for line in text.splitlines()]

    print(f"matching tails count: {len(hashes)}")

    matches = [count for t, count in hashes if t == tail]
    if (len(matches) == 0):
        return 0
    else:
        return matches[0]

    return count


# JR change to for loops etc as an exercise to understand the two original lines of code
def occurences_count_5(text, tail):
    print_function_name()

    lines = text.splitlines()

    hashes = []
    for line in lines:
        hashes.append(line.split(':'))

    count = 0
    for hash in hashes:
        (t, c) = hash
        if t == tail:
            print("Match:", t, tail, c)
            count = c
    return count


# JR change to for loops etc as an exercise to understand the two original lines of code
def occurences_count_6(text, tail):

    # hashes = (line.split(':') for line in text.splitlines())
    # count = next((int(count) for t, count in hashes if t == tail), 0)

    print_function_name()

    def hashes():
        for line in text.splitlines():
            yield (line.split(':'))
    
    def matches():
        for t, count in hashes():
            if t == tail:
                yield count

    # only expecting one result, so only one call to next()
    count = next(matches(), 0)
    return count


def main(args):
    print(__file__)
    print(f"Arguments count: {len(sys.argv)}")
    for i, arg in enumerate(sys.argv):
        # JR greater than 6 is just spacing of print output
        print(f"Argument {i:>6}: {arg}")

    ec = 0
    for pwd in args or sys.stdin:
        pwd = pwd.strip()
        if pwd == "":
            pwd = "farside111"
            print(f"using {pwd} as default for testing")

        try:
            sha1pwd, count = lookup_pwned_api(pwd)
        except UnicodeError:
            errormsg = sys.exc_info()[1]
            print("{0} could not be checked: {1}".format(pwd, errormsg))
            ec = 1
            continue

        if count:
            foundmsg = "{0} was found with {1} occurrences (hash: {2})"
            print(foundmsg.format(pwd, count, sha1pwd))
            ec = 1
        else:
            print("{} was not found".format(pwd))
    return ec


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
