"""Products and intervals the MMS shots share."""
from SciQLop.user_api import TimeRange

BURCH_EDR = TimeRange("2015-10-16T13:05:25", "2015-10-16T13:07:35")
MMS_DAY = TimeRange("2015-10-16T00:00", "2015-10-17T00:00")
SHEATH_TO_MSPHERE = TimeRange("2015-10-16T10:00", "2015-10-16T16:00")

DIS_BRST = "speasy//cda//MMS//MMS1//DIS//MMS1_FPI_BRST_L2_DIS_MOMS//"
DIS_FAST = "speasy//cda//MMS//MMS1//DIS//MMS1_FPI_FAST_L2_DIS_MOMS//"
FGM_BRST_GSM = "speasy//cda//MMS//MMS1//FGM//MMS1_FGM_BRST_L2//mms1_fgm_b_gsm_brst_l2"
FGM_SRVY_GSM = "speasy//cda//MMS//MMS1//FGM//MMS1_FGM_SRVY_L2//mms1_fgm_b_gsm_srvy_l2"
FGM_SRVY_POS_GSM = "speasy//cda//MMS//MMS1//FGM//MMS1_FGM_SRVY_L2//mms1_fgm_r_gsm_srvy_l2"
