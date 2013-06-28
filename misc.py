
def date_to_mysqlDate(inDateString):
    """ changes dates from the scraped data in MM/DD/YYYY to 
        MySQL-ready date format strings YYYY-MM-DD """

    yySplit = map(str, inDateString.split('/'))
    return '-'.join([yySplit[-1],yySplit[0],yySplit[1]])

def getYear(inDateString):
    """ returns release year from release date """

    if '/' in inDateString:
        inDateString = date_to_mysqlDate(inDateString)

    yySplit = map(str, inDateString.split('-'))

    return yySplit[0]
