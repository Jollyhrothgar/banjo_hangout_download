# banjo_hangout_download

Scraping tabs posted to the banjo hangouts archive.

This is a minimally functional version that has cached about 2,000 tabs from the
banjo hangout archive that were parsable from the various lists.

There are about 8,000 total tabs, six thousand are not included here due to:

*   Errors parsing the html cache
*   Tabs are not in TablEdit format (TEF)
*   There was an error downloading the tab, due to a server timeout or malformed
    file

I've parsed whatever data is available for each tab, which is broadly:

*   Genre (Bluegrass, Country, Old Time, Jazz, etc)
*   Style (Clawhammer, Scruggs, Old Time, etc)
*   Title (usually whatever the user input)
*   Tuning (should be also obvious from the tab)

The data is pretty messy still (but almost there!). I parsed everything using a
combination of `requests`, `Beautiful Soup` and regular expressions, but the
regular expressions need to be tuned a bit more. Each `div` has been identified
by getting a list of all `div`s containing tab links, and then regular
expressions are used to parse out the details. Here's an example of the data
container:

![Container](img/hangout_example.png)
