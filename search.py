#!/usr/bin/env python

from elasticsearch import Elasticsearch, helpers
from optparse import OptionParser
import curses
import json
import signal,sys

def catch_ctrl_C(sig,frame):
    print("CTRL + c is disabled. Press q to exit!")

def main():
    parser = OptionParser(usage="usage: %prog [options] filename",
                          version="%prog 1.0")
    parser.add_option("-s", "--source",
                      dest="source",
                      help="...")

    parser.add_option("-f", "--format",
                      dest="format",
                      help="json")

    (options, args) = parser.parse_args()

    # if len(args) != 1:
    #     parser.error("wrong number of arguments")

    # print(options)
    # print(args)

    signal.signal(signal.SIGINT, catch_ctrl_C)

    vulnerable = []
    if options.format == 'json':
        print('Sourcing from file')

        try:
            es = Elasticsearch(hosts=["192.168.0.200:30001"])

            scr = curses.initscr()
            curses.cbreak()
            scr.addstr(3, 0, "Progress % | Examinated | Vulnerable")

            with open(options.source) as data:
                data = json.load(data)
                data_len = len(data)
                # print("Looking over {} user passwords".format(len(vulnerable)))
                cnt = 0
                vulnerable_cnt = 0
                for l in data:
                    cnt +=1
                    if cnt >= 100:
                        break
                    user_request = "some_param"

                    query_body = {
                      "query": {
                        "bool": {
                          "must": {
                            "match": {
                              "md5": l['password']
                            }
                          }
                        }
                      }
                    }

                    result = es.search(index="passwords", body=query_body)

                    found = result['hits']['hits']

                    if len(found) != 0:
                        password = result['hits']['hits'][0]['_source']['password']
                        vulnerable.append({"username": l['username'], "password": password})
                        vulnerable_cnt += 1
                    count_percentage = (cnt / data_len ) * 100

                    scr.addstr(0, 0, "Looking over {} entries".format(data_len))
                    scr.addstr(4, 1, str(round(count_percentage, 2)))
                    scr.addstr(4, 13, str(cnt))
                    scr.addstr(4, 26, str(vulnerable_cnt))

                    scr.addstr(6, 0, "Press q to stop")
                    scr.addstr(8, 0, "") # keeping this line for CTRL + c message
                    scr.refresh()

                    # Catching exit signal
                    scr.nodelay(1)
                    c = scr.getch()
                    if c == ord('q'):
                        curses.endwin()
                        curses.beep()
                        break

            curses.endwin()

            # print("Found {} known passwords over {} entries".format(len(vulnerable), data_len))
            print("\n\nSummary:")
            print(f"Completed:  {round(count_percentage, 2)}%")
            print(f"Entries:    {data_len}")
            print(f"Vulnerable: {vulnerable_cnt}")

        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

if __name__ == '__main__':
    main()
