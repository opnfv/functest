#!/usr/bin/env python
# fpj@redhat.com
# yfried@redhat.com


import sys


class Segment(object):

    def __init__(self, start=0, end=0, segment=None):
        if segment:
            self.start = segment.get_start()
            self.end = segment.get_end()
        else:
            self.start = start
            self.end = end

    def get_start(self):
        return self.start

    def get_end(self):
        return self.end

    def set_end(self, end):
        self.end = end

    def __str__(self):
        return ("Segment starts: %s, ends: %s" % (self.start, self.end))


def main():
    # single example
    segment1 = Segment(1, 10)
    segment2 = Segment(9, 20)  # intersection with the previous one
    segment3 = Segment(30, 50)
    segment4 = Segment(40, 80)  # intersection with the previous one #
    segment5 = Segment(82, 100)
    input_list = [segment1, segment2, segment3, segment4, segment5]

    # consider all the possibilities
    segment1 = Segment(0, 10)
    segment2 = Segment(9, 40)
    segment3 = Segment(20, 30)
    segment4 = Segment(38, 50)
    segment5 = Segment(60, 70)
    segment6 = Segment(80, 90)
    segment7 = Segment(85, 100)
    input_list = [segment1, segment2, segment3,
                  segment4, segment5, segment6, segment7]

    # just for output information
    print("INPUT LIST:")
    for segment in input_list:
        print(segment)

    # algorithm:
    output_list = []

    overlay = Segment(segment=input_list[0])
    output_list.append(overlay)

    for i in xrange(1, len(input_list)):
        item = input_list[i]

        # overlap
        if (overlay.get_end() >= item.get_start()):
            overlay.set_end(max(overlay.get_end(),
                                item.get_end()))
        else:
            overlay = Segment(segment=item)
            output_list.append(overlay)

    print("\nOUTPUT LIST:")
    for segment in output_list:
        print(segment)


if __name__ == '__main__':
    sys.exit(main())
