#!/usr/bin/env python

from elasticsearch import Elasticsearch, helpers
from optparse import OptionParser
import glob

def main():
    parser = OptionParser(usage="usage: %prog [options] filename",
                          version="%prog 1.0")
    parser.add_option("-s", "--source",
                      # action="store_true",
                      dest="source",
                      # default=False,
                      help="create a XHTML template instead of HTML")

    parser.add_option("-b", "--batchsize",
                      # action="store_true",
                      dest="batchsize",
                      default=10000,
                      help="create a XHTML template instead of HTML")


    parser.add_option("-c", "--cssfile",
                      action="store", # optional because action defaults to "store"
                      dest="cssfile",
                      default="style.css",
                      help="CSS file to link",)
    (options, args) = parser.parse_args()

    # if len(args) != 1:
    #     parser.error("wrong number of arguments")

    # print(options)
    # print(args)

    if options.source == 'file':
        print('Sourcing from file')
        sources = glob.glob("password_source/*")
        for source in sources:
            print("    - {}".format(source))
            try:
                passwords = []
                with open(source) as fp:
                    line = fp.readline()
                    cnt = 0
                    while line:
                        # print("Line {}: {}".format(cnt, line.strip()))
                        line = fp.readline()
                        passwords.append(line)
                        cnt += 1

                batch(passwords, options.batchsize)
                print("Processed {} passwords".format(cnt))

            finally:
                fp.close()


def batch(passwords, batchsize):
    print("Total passwords: {}".format(len(passwords)))
    print("Batch size: {}".format(batchsize))
    import hashlib
    cnt = 0
    batch_n = 0
    batch = []
    for password in passwords:
        cnt += 1
        hashed_password = hashlib.md5(
            password.encode("raw_unicode_escape").strip().lower()
        ).hexdigest()

        batch.append({
            "_index": 'passwords',
            '_op_type': 'index',
            "_type": "_doc",
            'password': password, 'md5': hashed_password
        })

        if cnt == batchsize:
            print('    sending batch {}'.format(batch_n))
            send_batch(batch)
            batch = []
            batch_n += 1
            cnt = 0

    # Sending remaing
    send_batch(batch)


def send_batch(batch):
    es = Elasticsearch(
        ['192.168.0.200'],
        port=30001
    )
    helpers.bulk(es, batch)


if __name__ == '__main__':
    main()
