
import numpy as num


def RobustMedianSigma(indata, cutoff):
    """ Computes an outlier rejected mean or median of a data array.
        Based on the robust median, and mean calculator robustmm.
        Inputs
        indata - numpy data array
        cutoff - number, such as 3,4 or 5 sigma clipping values
        """

    indata = num.array(indata)
    med = num.median(indata.ravel())
    absdev = abs(indata-med)
    #compute median absolute deviation
    medabsdev = num.median(absdev)

    # check if cutoff is too small
    if cutoff < 1.0:
        #print 'Warning: Truncation might remove useful points.
        #Setting cutoff to 1-sigma.'
        cutoff = 1.0
    else:
        cutoff = cutoff
    
    sc = cutoff*medabsdev/0.6745e0

    # indicies of reasonable values
    goodindex = num.where(absdev <= sc)[0]

    # indicies of outliers
    badindex = num.where(absdev > sc)[0]

    # compute median
    mm = num.median(indata[goodindex])
    sdv = num.std(indata[goodindex])
        
    return mm, sdv, goodindex, badindex

def returnSuccessMetric(gross,budget):
    """  return the success metric """

    # sM (success metric), which is essentially
    # the profit margin
    sM = (gross - budget)/gross
    # change -inf values to zeros
    indx_zeros = num.where(sM == num.float('-inf'))[0]
    sM[indx_zeros] = 0e0

    return sM

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
