

def getFeatureCdByCode(code):
    if code.startswith('1002'):
        return 2
    if code in '122101' or code == '224102' or code == '224104':
        return 5
    if code in ['112101', '112102', '1122', '1123', '1131', '122102', '220101', '220102', '2202', '2203', '224103',
                '224105', '4001']:
        return 4
    return 1
