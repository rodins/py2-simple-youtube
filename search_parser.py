# -*- coding: UTF-8 -*-

class SearchParser:

    def find_value(self, key, line):
        offset = len(key)+4
        begin = line.find(key)
        end = line.find("\"", begin+offset+1)
        if begin != -1 and end != -1:
            value = line[begin+offset:end]
            return value
        else:
            return ""

    def parse(self, response):
        is_item = False
        for line in response:
            value = self.find_value("nextPageToken", line)
            if value != "":
                next_page = value
                continue

            value = self.find_value("videoId", line)
            if value != "":
                is_item = True
                video_id = value
                continue
            value = self.find_value("title", line)
            if value != "":
                title = value
                continue
            value = self.find_value("url", line)
            if value != "":
                url = value
                if is_item:
                    is_item = False
                    #print "Add to model..."
                    print title
                    print video_id
                    print url
                    print
        print "Next page..."
        print next_page
