#!/usr/bin/env python

import re

"""
This is not optimized, it loads the text files for every single request, and
uses regexps on them to find something. A persistent script and an optimized
binary index would be a lot faster of course.

The allegro.devhelp is generated by "make docs-devhelp" in the allegro dir. The
agl.hhk is the file html/index.hhk generated by running doxygen in the allegrogl
dir.
"""

#allegro_url = "http://allefant/web/allegro/html"
allegro_url = "http://www.liballeg.org/stabledocs/en/"
allegro_gl_url = "http://allegrogl.sourceforge.net/docs"

#hhk_path = "agl.hhk"
hhk_path = "/home/groups/a/al/allegrogl/htdocs/docs/index.hhk"

def search(text, onlink):
    try:
        lines = file ("allegro.devhelp").readlines()
        for line in lines:
            match = re.compile (".*?<sub name=\"(.*?" + re.escape(text) +
                ".*?)\" link=\"(.*?)\"", re.I).match (line)
            if match:
                link = (match.group(1), allegro_url + "/" + match.group(2))
                onlink(link)
    except IOError:
        pass

    try:
        lines = file (hhk_path).readlines()
        for i in range ( len(lines)):
            match = re.compile("  <LI><OBJECT type=\"text/sitemap\"><param name=\"Local\" value=\"(.*?)\">" +
                "<param name=\"Name\" value=\"(.*?" + re.escape(text) +
                ".*?)\"></OBJECT>", re.I).match(lines[i])
            if match:
                page = match.group(1)
                link = (match.group(2), allegro_gl_url + "/" + page)
                onlink(link)
    except IOError:
        pass

def apisearch(query):
    print "Content-Type: text/html"
    print
    print "<html>"
    print "<header><title>%s</title>" % "Search Results"
    print "</header>"
    print "<body>"
    print '''\
<form action="search.py" method="get">
<input type="text" name="query" value="%s" />
<input type="submit" name="submit" value="Query">
</form>''' % query
    if query:
        got_links = [0]
        print "<h1>Results for \"%s\"</h1>" % query
        def onlink(link):
            print '<li><a href="%s">%s</a></li>' % (link[1], link[0])
            got_links[0] += 1
        print "<ul>"
        search(query, onlink)
        print "</ul>"
        print "%d results found." % got_links[0]
    else:
        print "<h1>No search performed</h1>"
    print "</body></html>"

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        print "Searching for \"%s\" from commandlne." % sys.argv[1]
        def onlink(link): print link
        search(sys.argv[1], onlink)
    else:
        import cgi, urllib, cgitb; cgitb.enable()
        form = cgi.FieldStorage()

        if form.has_key("query"):
            query = form["query"].value
        else:
            query = ""

        if form.has_key("where"):
            where = form["where"].value
        else:
            where = ""

        if where == "mail":
            print "Location: " + \
                "http://sourceforge.net/search/?" + \
                "type_of_search=mlists&exact=1&" + \
                "forum_id=34598&group_id=5665&atid=0&" + \
                "words=%s&Search=Search" % urllib.quote_plus(query)
            print
        elif where == "site":
            print "Location: " + \
                    "http://google.com/search?q=site:alleg.sourceforge.net+" + \
                    urllib.quote_plus(query)
            print
        elif where == "forum":
            print "Location: " + \
                "http://www.allegro.cc/forums/search.php?member_id=0&" + \
                "keywords=%s&" % urllib.quote_plus(query) + \
                "member_name=&order=rel&forum_all=1"
            print
        else:
            apisearch(query)

