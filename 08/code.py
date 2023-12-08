import argparse
from time import time
import itertools
import re
import math

DAY = 8

PUZZLE_TEXT = '''
'''

P1_SAMPLE_INPUT = '''
LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)
'''

P2_SAMPLE_INPUT = '''
LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
'''

PUZZLE_INPUT = '''
LRRLRRLLRRRLRRLRLRRRLRRLRRRLRLLRRRLRRRLRLRRRLRRLRRLRLRLLLRRRLRRRLRRLRRLRLRRRLRRLLRRLRRLRLLRLRLRRLRLLRLRLRRRLRRLRLLRLRLLRRLRLRRLLLRLRRLRRRLLLRRLRLRRRLLRRLLLRRRLRRRLLLRRLLRLRRLRLRRLLLRLRRLLLLRRLLRRRLRRLRRLRLRLLRLRRRLLRRLLRRLRRLRRLRRLRLLRRLRRRLRLRLLLRRRLLRRRLRRLRRLLLLRRRR

VRN = (CSM, GPD)
XDT = (QBK, PJR)
HVC = (MKM, TJS)
KRH = (BHN, PXB)
GTX = (VFD, TXR)
BQB = (MQV, PFQ)
TDV = (VSG, MJX)
VJM = (QHP, XMB)
KLG = (QLJ, HCV)
TSM = (JPG, DNP)
KHS = (QNR, DXJ)
FXM = (PHF, PHF)
RMV = (BMM, KHS)
QXL = (BKG, TLP)
MHS = (QXL, CFQ)
TBT = (TVT, BRD)
QXS = (GPP, RND)
XLL = (JHQ, LDV)
PBQ = (VXK, RJR)
FXB = (HMN, THX)
DPF = (GLX, GNC)
HVG = (HJF, SCH)
QMN = (DQJ, GMN)
MBS = (PFX, JHG)
VGL = (FHX, CCK)
QLV = (BLT, FDR)
MNS = (BDB, BMJ)
MMT = (TSM, SFR)
NRP = (FKB, QPH)
XFQ = (GTS, CCQ)
XFF = (HKG, NVL)
TXR = (VHQ, CKP)
VPL = (GHC, VMT)
SGC = (BGM, MJV)
SMS = (GJV, LSC)
BVC = (PRH, FJJ)
JHQ = (VJQ, XTX)
RJF = (GKK, NKX)
RJR = (JJQ, JTK)
VHQ = (JPS, JPS)
SFR = (JPG, DNP)
RDP = (GPD, CSM)
GGQ = (MVX, XBP)
XGK = (GBB, VPH)
XBH = (PTH, GSL)
MKG = (RBP, MGG)
FSG = (KFC, RMB)
NHC = (RQG, CVF)
SSV = (MVF, QFP)
RLP = (FXC, HCP)
FBZ = (FJF, CRJ)
HFL = (FKB, QPH)
NBM = (QBD, XGK)
NSP = (QKG, NDN)
TQF = (RMH, TDB)
RBB = (QTC, HPT)
CVF = (BSV, VTR)
XQG = (LFJ, JXD)
KXF = (CRJ, FJF)
MQC = (MQL, BSL)
RCC = (NHC, QLC)
TNT = (VKQ, NSX)
TVN = (NDN, QKG)
SCH = (FXB, NTM)
CVD = (XLJ, XDT)
QVF = (MQR, RDB)
GXS = (HCK, SHD)
KBD = (JHG, PFX)
KXV = (HVQ, QCJ)
MQR = (RNQ, SVC)
CBC = (SXB, BVC)
GKK = (HDR, LTF)
FRT = (CFQ, QXL)
VMT = (SQQ, DBB)
QPV = (NVQ, VVV)
XGD = (MPL, PMQ)
MNT = (JDD, NQC)
RGT = (QHD, SQP)
HXV = (RQD, RRX)
LGR = (FHX, CCK)
PHF = (CBV, TMC)
BTP = (JSC, QMN)
CXS = (SCH, HJF)
MQV = (FGJ, QPD)
HRZ = (CCX, BCF)
DDB = (DJK, CVD)
XNL = (QLJ, HCV)
GLX = (MGN, CFV)
QCJ = (NDK, XBR)
XBX = (CQM, VKD)
QPH = (XBH, CFG)
NSL = (LFJ, JXD)
DJQ = (VMN, STS)
RNV = (XFF, KSR)
JTR = (QLG, XRD)
VVV = (MDH, KHK)
TLR = (DMH, NXC)
GBH = (GLS, XLK)
LRN = (QRM, FMC)
BRM = (DCK, DSK)
GQS = (FXV, QPV)
XMT = (NHF, RXG)
KLR = (HFN, KDR)
SVH = (RMR, JLC)
QSG = (KQC, CMH)
VVX = (XGM, FNX)
BCF = (LNR, MTS)
RPJ = (RCC, CKG)
JJD = (NRP, HFL)
FGP = (MFS, RBB)
BJX = (BTD, KSC)
PQC = (VMN, STS)
JPG = (RQL, CSQ)
SLK = (JJC, BPJ)
JTK = (XHN, BFH)
HCV = (BRF, VPT)
VPH = (BVS, RRT)
MSH = (JQF, XFJ)
JHL = (QPF, QPF)
FGD = (MPC, TVB)
DCB = (JBC, XFB)
RKN = (TSL, VQG)
QBQ = (QLV, NRT)
MQX = (JSX, MCV)
XHX = (FNX, XGM)
DTL = (JDM, BDX)
LST = (JHL, CQN)
VGR = (HQV, HRZ)
CTQ = (XCF, TJK)
SQP = (HHB, NBM)
RRL = (TSL, VQG)
NNM = (DDS, XSF)
KHK = (HSG, NDF)
MGN = (VXT, VGV)
TLB = (DPK, MLV)
NMM = (TRR, XJH)
SJG = (XRJ, XBX)
GSC = (RRL, RKN)
KDR = (PSJ, TBM)
LRP = (SQP, QHD)
DKF = (MVR, QQB)
FHC = (BPT, BKC)
PLT = (JGG, GGQ)
XRD = (HMH, PBQ)
RHP = (JPD, XVL)
MXF = (MQR, RDB)
DML = (BRD, TVT)
CKP = (JPS, RBS)
BFK = (BCL, TLK)
KSR = (NVL, HKG)
XQF = (BMM, KHS)
BVJ = (CBL, PLC)
BCS = (RQF, GTB)
JCC = (VTT, VPQ)
BCL = (BNV, PDB)
HCK = (DDB, CBX)
SVG = (FGD, VQL)
BLT = (XNK, LHM)
MVQ = (LRG, NPB)
RND = (QCK, QRN)
HFR = (FBT, CLS)
KNK = (XDS, BCK)
XBB = (BRM, FDC)
XGM = (FFC, GJX)
PTN = (TQF, QKP)
RNQ = (GSC, XKH)
TPT = (CMK, KXT)
HPL = (CKB, QLR)
MVX = (QSG, TKJ)
QFP = (RLP, RSF)
GXF = (LNB, VNJ)
QHD = (NBM, HHB)
KSS = (LLH, PFK)
MFD = (XGJ, GGS)
JJQ = (XHN, BFH)
JDD = (HXV, FVH)
CFR = (FXM, FXM)
FDR = (XNK, LHM)
DHG = (BRS, TLR)
TDB = (SBS, XBB)
BVS = (GQH, BFS)
DGZ = (TMC, CBV)
HQD = (JSC, QMN)
TMZ = (XFB, JBC)
BRF = (MBF, KGJ)
RQG = (VTR, BSV)
CSQ = (FTS, RHR)
FFJ = (QCL, CTQ)
XKH = (RRL, RKN)
VJQ = (BTL, GQS)
NGK = (JGG, GGQ)
RQN = (GVG, SJN)
GRR = (RNV, FHF)
LSR = (VBL, SLK)
VQG = (QBV, NJV)
BHK = (BVJ, LJR)
BRS = (DMH, NXC)
NKX = (LTF, HDR)
QBD = (GBB, VPH)
RGQ = (CLM, FHK)
VXX = (KRH, VGN)
KRF = (VFQ, SMN)
XFR = (XGD, RMM)
JGC = (JGM, PFR)
SHD = (DDB, CBX)
QKG = (QTS, GXP)
CDL = (GLX, GNC)
RBP = (HKK, CMN)
CLN = (HDG, BHM)
XFX = (RNV, FHF)
AAA = (DXX, SVG)
FXC = (MMT, KLS)
PTF = (SKF, SDF)
QPF = (RQF, RQF)
DTB = (HQV, HQV)
RRF = (FNV, MKG)
MGG = (HKK, CMN)
NDF = (KMD, FFH)
DVL = (RKL, CLC)
JRQ = (BXV, BRB)
HVM = (DRT, SSV)
BHM = (KNK, BPP)
TDT = (DPS, VCP)
JPC = (DCH, FHD)
RSF = (FXC, HCP)
KSX = (BVJ, LJR)
NLT = (LTB, QBQ)
SBD = (NKX, GKK)
VQL = (MPC, TVB)
JXD = (MLK, LHN)
XNN = (TNT, LPQ)
HMH = (RJR, VXK)
JGG = (MVX, XBP)
PTP = (MVQ, NPS)
FQC = (XQF, RMV)
FXT = (TDH, JGD)
RGP = (CPN, KGF)
BTD = (NKN, NTQ)
BGM = (NRJ, CJN)
RMM = (PMQ, MPL)
DQJ = (DPF, CDL)
TVT = (TFJ, VJM)
TGL = (CGS, SJG)
NHF = (HVC, LVM)
NMK = (GRR, XFX)
QRN = (MMP, XSL)
FFH = (DJQ, PQC)
PDJ = (NQC, JDD)
CGS = (XBX, XRJ)
NTQ = (RXX, FLX)
CFB = (TVC, PTP)
GXK = (FLC, GXS)
RBS = (DCB, TMZ)
CFQ = (TLP, BKG)
QHP = (KVX, GSG)
HDJ = (RPH, QPK)
VXT = (GXF, JKM)
NCM = (NJL, TGL)
HFN = (TBM, PSJ)
JGF = (CFB, NMC)
JDM = (CLN, PHJ)
DJS = (RMR, JLC)
RDB = (RNQ, SVC)
RRX = (HQD, BTP)
HHS = (MXF, QVF)
MMP = (GTX, HKC)
JRK = (KKP, PTN)
TRR = (VGD, HGC)
JKM = (LNB, VNJ)
BRD = (TFJ, VJM)
TLK = (BNV, PDB)
QTS = (CHL, LSR)
BPP = (XDS, BCK)
RXX = (BKP, TLS)
VFD = (VHQ, VHQ)
BQF = (DHG, DQC)
XDL = (QVF, MXF)
ZZZ = (SVG, DXX)
GGB = (LTB, QBQ)
QTN = (JHL, CQN)
BVK = (BHQ, SSG)
VGB = (BXV, BRB)
QLR = (XFR, KNM)
QBK = (KNC, VJX)
BMJ = (JLK, TDV)
FDC = (DSK, DCK)
XDS = (SMS, TVR)
GBC = (NGK, PLT)
HPT = (XHQ, SXT)
FHK = (JCC, FJS)
KNM = (RMM, XGD)
GTB = (KLR, JVZ)
VCT = (PTN, KKP)
LDV = (XTX, VJQ)
KTK = (MQV, PFQ)
TVC = (MVQ, NPS)
BXV = (XLL, KDL)
BFA = (BCF, CCX)
CCF = (CLM, FHK)
JGS = (VCP, DPS)
RVK = (MKJ, QLH)
FNX = (FFC, GJX)
XBP = (QSG, TKJ)
LMJ = (FPH, JVL)
HKG = (VXX, RNX)
KMD = (DJQ, PQC)
BRB = (XLL, KDL)
NDK = (DJS, SVH)
BSV = (XVC, QXS)
TLS = (FSJ, MNS)
CRJ = (SGC, RNH)
BNV = (QSF, FSG)
SMN = (MNK, QGN)
JVV = (TRN, DVL)
JJC = (HBT, RPJ)
KSB = (XVL, JPD)
JJT = (TLB, DTJ)
TSL = (QBV, NJV)
GNV = (GCS, JLR)
HJF = (FXB, NTM)
VMN = (CFR, CFR)
GVG = (XDL, HHS)
LNB = (HMP, XMP)
RTL = (FXT, RCT)
XVC = (RND, GPP)
GNS = (MFS, RBB)
XTG = (LRM, DKQ)
JVZ = (KDR, HFN)
QQB = (XTG, GFG)
HMN = (FHC, FMN)
XLC = (FXT, RCT)
CKG = (QLC, NHC)
NJB = (DVL, TRN)
VCP = (LRF, HPL)
KQJ = (MXH, MXH)
GJV = (TPT, QNJ)
CCX = (LNR, MTS)
DTJ = (MLV, DPK)
HDX = (JSX, MCV)
XRJ = (VKD, CQM)
DMH = (RGP, KPR)
QGN = (VRF, QDL)
JSC = (DQJ, GMN)
BPT = (LLB, XNN)
CJN = (JJT, PGM)
XDV = (XVD, HJH)
JHG = (LLF, MLJ)
NKN = (FLX, RXX)
TGP = (XJH, TRR)
TLP = (XLC, RTL)
HQT = (SSN, BPS)
BKP = (MNS, FSJ)
VPT = (KGJ, MBF)
JSJ = (PFK, LLH)
CBX = (DJK, CVD)
TJK = (VGL, LGR)
THP = (TGL, NJL)
NSX = (SQL, GNV)
JQF = (VDM, JJD)
SDF = (JPC, KRV)
XNK = (HDJ, MQJ)
DSD = (SJN, GVG)
SBS = (FDC, BRM)
FPH = (NCM, THP)
LMR = (KQJ, BGV)
VKQ = (SQL, GNV)
FMC = (CPV, GBC)
HHB = (QBD, XGK)
HVQ = (NDK, XBR)
KXT = (JKG, NLS)
GJX = (TVP, JTR)
JLT = (MHM, MSH)
VNJ = (HMP, XMP)
TDH = (JGF, GGD)
VPQ = (HDX, MQX)
SKF = (JPC, KRV)
NXT = (RXG, NHF)
TRN = (CLC, RKL)
RRT = (BFS, GQH)
JFJ = (SXB, BVC)
KBR = (CGD, JGC)
PGG = (HFR, TJJ)
CMK = (JKG, NLS)
CBV = (FCX, KBR)
GMN = (DPF, CDL)
BTL = (QPV, FXV)
PFX = (MLJ, LLF)
DCT = (XLK, GLS)
PGM = (DTJ, TLB)
NVL = (VXX, RNX)
RPD = (TLK, BCL)
QDL = (FFJ, SFH)
JVL = (THP, NCM)
NVQ = (MDH, KHK)
TMC = (FCX, KBR)
LPQ = (NSX, VKQ)
RHR = (PPL, LCD)
JSX = (DHM, PMS)
DPK = (KBD, MBS)
LTF = (PGG, QPN)
BPS = (GXK, HCM)
HKC = (VFD, TXR)
PXB = (RPN, BQF)
FLX = (TLS, BKP)
PJR = (VJX, KNC)
PDB = (QSF, FSG)
NMC = (TVC, PTP)
MLP = (MSH, MHM)
PMQ = (KXV, QFJ)
FKB = (XBH, CFG)
JRV = (SMN, VFQ)
SQL = (GCS, JLR)
DXX = (FGD, VQL)
XMM = (GMG, LRN)
PFK = (HDL, XFQ)
XSL = (GTX, HKC)
CLC = (JRQ, VGB)
LMH = (KXF, FBZ)
NMX = (KSC, BTD)
GTJ = (KLG, XNL)
THX = (FMN, FHC)
RMH = (XBB, SBS)
SSG = (MFD, KFP)
QNR = (RBG, HNG)
DSK = (LMJ, FRP)
GQP = (FXM, XVT)
MFS = (QTC, HPT)
VHX = (VBD, RDD)
SQS = (GTJ, MSR)
LJR = (CBL, PLC)
QSF = (KFC, KFC)
DHM = (VFJ, DTL)
MDH = (NDF, HSG)
SSN = (HCM, GXK)
HCM = (FLC, GXS)
PQX = (FGG, BXR)
DQC = (BRS, TLR)
KRV = (DCH, FHD)
FNH = (SKF, SDF)
LFJ = (LHN, MLK)
MVR = (GFG, XTG)
HBT = (RCC, CKG)
VKD = (NMK, PFV)
TKJ = (KQC, CMH)
MRH = (RHV, ZZZ)
CKB = (XFR, KNM)
BMM = (DXJ, QNR)
KDL = (JHQ, LDV)
VFJ = (BDX, JDM)
PLC = (PND, GNP)
MNK = (QDL, VRF)
MXT = (RMV, XQF)
TJS = (PTF, FNH)
PHJ = (BHM, HDG)
FSJ = (BDB, BMJ)
CFV = (VGV, VXT)
XVD = (CBF, SQS)
TFJ = (QHP, XMB)
CPV = (PLT, NGK)
VTR = (XVC, QXS)
BKC = (XNN, LLB)
NPS = (NPB, LRG)
FXV = (NVQ, VVV)
FTS = (PPL, LCD)
HMP = (QMD, SNX)
VBD = (DTB, DTB)
VFQ = (QGN, MNK)
KFP = (GGS, XGJ)
BHN = (RPN, BQF)
PFV = (GRR, XFX)
QMD = (MGK, XDV)
MLK = (RPD, BFK)
GFG = (DKQ, LRM)
NLS = (BQB, KTK)
XLK = (HVG, CXS)
LSC = (QNJ, TPT)
FNV = (RBP, MGG)
HKK = (RCX, MQC)
GPD = (NSL, XQG)
RQL = (RHR, FTS)
HDB = (GHC, VMT)
HJH = (SQS, CBF)
QTC = (SXT, XHQ)
TRS = (BXR, FGG)
MTS = (DML, TBT)
RHV = (DXX, SVG)
XVL = (FGP, GNS)
GSG = (RRF, CSP)
VBL = (JJC, BPJ)
CCK = (RJF, SBD)
QPN = (TJJ, HFR)
PRH = (TGP, NMM)
PQT = (TRS, PQX)
QKP = (RMH, TDB)
XMP = (SNX, QMD)
QPD = (KRF, JRV)
RQD = (HQD, BTP)
XVT = (PHF, DGZ)
GXP = (CHL, LSR)
LHM = (MQJ, HDJ)
STS = (CFR, GQP)
FJJ = (NMM, TGP)
MPC = (CCF, RGQ)
MKM = (PTF, FNH)
QVH = (VBD, VBD)
XMB = (KVX, GSG)
CHL = (VBL, SLK)
XBR = (DJS, SVH)
KPR = (CPN, KGF)
MQL = (KSB, RHP)
CQM = (PFV, NMK)
XHQ = (HCR, HVM)
FFC = (JTR, TVP)
FMN = (BPT, BKC)
SNX = (MGK, XDV)
KNC = (QVJ, NNM)
DPS = (LRF, HPL)
GBB = (BVS, RRT)
BFH = (XMM, XQL)
GLS = (HVG, CXS)
RXG = (LVM, HVC)
MPL = (QFJ, KXV)
NXC = (KPR, RGP)
NJV = (TVN, NSP)
LLB = (LPQ, TNT)
SXT = (HVM, HCR)
LLH = (HDL, XFQ)
MLV = (KBD, MBS)
CBF = (GTJ, MSR)
JBC = (KTX, QQG)
FLC = (SHD, HCK)
FRP = (FPH, JVL)
BHQ = (MFD, KFP)
LNR = (DML, TBT)
CSP = (MKG, FNV)
GHC = (SQQ, DBB)
NRT = (BLT, FDR)
VTT = (HDX, MQX)
HSG = (FFH, KMD)
VGA = (CBV, TMC)
KLS = (TSM, SFR)
PFQ = (FGJ, QPD)
MKJ = (JLT, MLP)
MFX = (RVK, NSF)
QNJ = (KXT, CMK)
QBV = (NSP, TVN)
MSR = (KLG, XNL)
NSF = (QLH, MKJ)
DKQ = (JDR, DQQ)
PLH = (RVK, NSF)
JKG = (BQB, KTK)
LVM = (MKM, TJS)
QLJ = (VPT, BRF)
FVH = (RRX, RQD)
MJX = (DCT, GBH)
QLH = (MLP, JLT)
NPB = (XMT, NXT)
HDL = (CCQ, GTS)
JPS = (DCB, DCB)
CQN = (QPF, BCS)
GNP = (DSD, RQN)
JLK = (MJX, VSG)
PMS = (DTL, VFJ)
BFS = (JGS, TDT)
XJH = (VGD, HGC)
VRF = (SFH, FFJ)
BCK = (SMS, TVR)
DRT = (QFP, MVF)
PND = (DSD, RQN)
VSG = (GBH, DCT)
VGV = (JKM, GXF)
FHD = (MXT, FQC)
GPP = (QRN, QCK)
BDX = (CLN, PHJ)
LLF = (HQT, DCL)
DXA = (HFN, KDR)
MCV = (DHM, PMS)
NTM = (HMN, THX)
JLC = (RDP, VRN)
HQV = (BCF, CCX)
NDN = (QTS, GXP)
QVJ = (DDS, XSF)
MQJ = (RPH, QPK)
FGJ = (KRF, JRV)
LHN = (BFK, RPD)
MXH = (RHV, RHV)
HGC = (DNN, PQT)
MHM = (XFJ, JQF)
JGD = (JGF, GGD)
FCX = (JGC, CGD)
GCS = (LST, QTN)
RCX = (BSL, MQL)
XGJ = (VCT, JRK)
SXB = (FJJ, PRH)
LRG = (XMT, NXT)
XSF = (LRP, RGT)
DNP = (CSQ, RQL)
RKL = (VGB, JRQ)
KVX = (CSP, RRF)
JPD = (FGP, GNS)
GNC = (MGN, CFV)
PFR = (MHS, FRT)
DCK = (LMJ, FRP)
KKP = (TQF, QKP)
XQL = (GMG, LRN)
QCL = (TJK, XCF)
TVP = (XRD, QLG)
HDR = (QPN, PGG)
HLN = (BHQ, SSG)
GGS = (VCT, JRK)
SJN = (HHS, XDL)
DBB = (BHK, KSX)
QPK = (MFX, PLH)
MBF = (NLT, GGB)
BDB = (TDV, JLK)
KSC = (NKN, NTQ)
CPN = (HDB, VPL)
TVB = (RGQ, CCF)
VJX = (NNM, QVJ)
FBT = (JLL, LMR)
TVR = (GJV, LSC)
RNX = (KRH, VGN)
RPH = (MFX, PLH)
VJA = (JBC, XFB)
CLS = (JLL, LMR)
PSJ = (DKF, MSL)
QLG = (PBQ, HMH)
DXJ = (HNG, RBG)
XFB = (KTX, QQG)
TJJ = (FBT, CLS)
KFC = (JRF, JRF)
XFJ = (JJD, VDM)
RCT = (TDH, JGD)
RNH = (BGM, MJV)
VGD = (PQT, DNN)
KQC = (JFJ, CBC)
PPL = (JSJ, KSS)
HCR = (DRT, SSV)
XLJ = (PJR, QBK)
PTH = (QVH, VHX)
RQF = (KLR, KLR)
MSL = (MVR, QQB)
NRJ = (PGM, JJT)
JLL = (KQJ, KQJ)
DCL = (BPS, SSN)
GTS = (MNT, PDJ)
BXR = (NMX, BJX)
CBL = (PND, GNP)
VXK = (JJQ, JTK)
BSL = (RHP, KSB)
NJL = (SJG, CGS)
DQQ = (XHX, VVX)
SQQ = (BHK, KSX)
KTX = (BVK, HLN)
QCK = (XSL, MMP)
SVC = (GSC, XKH)
BGV = (MXH, MRH)
GMG = (QRM, FMC)
KGJ = (NLT, GGB)
LRF = (QLR, CKB)
CMN = (RCX, MQC)
CGD = (JGM, PFR)
LCD = (JSJ, KSS)
HDG = (BPP, KNK)
DDS = (LRP, RGT)
LRM = (DQQ, JDR)
CMH = (CBC, JFJ)
GQH = (TDT, JGS)
BKG = (RTL, XLC)
RMR = (VRN, RDP)
MGK = (XVD, HJH)
FJS = (VTT, VPQ)
SFH = (CTQ, QCL)
XHN = (XQL, XMM)
BPA = (CRJ, FJF)
XCF = (VGL, LGR)
TBM = (MSL, DKF)
JLR = (LST, QTN)
QFJ = (HVQ, QCJ)
CCQ = (MNT, PDJ)
VGN = (PXB, BHN)
LTB = (QLV, NRT)
DCH = (MXT, FQC)
CFG = (PTH, GSL)
JRF = (KXF, KXF)
QRM = (CPV, GBC)
XTX = (BTL, GQS)
FHX = (SBD, RJF)
FHF = (KSR, XFF)
CSM = (NSL, XQG)
HCP = (MMT, KLS)
DJK = (XDT, XLJ)
QLC = (CVF, RQG)
MLJ = (HQT, DCL)
CLM = (JCC, FJS)
NQC = (HXV, FVH)
RDD = (DTB, VGR)
RPN = (DQC, DHG)
GSL = (QVH, VHX)
FGG = (NMX, BJX)
BPJ = (RPJ, HBT)
RBG = (NJB, JVV)
FJF = (SGC, RNH)
GGD = (CFB, NMC)
QQG = (HLN, BVK)
MVF = (RLP, RSF)
JGM = (MHS, FRT)
RMB = (JRF, LMH)
VDM = (HFL, NRP)
HNG = (NJB, JVV)
MJV = (CJN, NRJ)
DNN = (PQX, TRS)
JDR = (XHX, VVX)
KGF = (HDB, VPL)
'''

P1_SAMPLE_SOLUTION = 6

P2_SAMPLE_SOLUTION = 6

def elapsed_time(start_time):
    return f"{round(time() - start_time, 8)}s\n"

class Puzzle():
    def __init__(self,input_text):
        self.input_text = input_text
        self.input_list = input_text.strip().split('\n')
        
                
    def p1(self):
        self.nodes = {}
        self.instructions = []
        for line in self.input_list:
            if '=' in line:
                readline = re.match(r"^(?P<node>[A-Z]{3}) = \((?P<left>[A-Z]{3}), (?P<right>[A-Z]{3})\)",line)
                self.nodes[readline.group('node')] = [readline.group('left'), readline.group('right')]
            else:
                for char in line:
                    self.instructions.append(char)
        self.p1_solution = 0
        current_node = 'AAA'
        while current_node != 'ZZZ':
            for step in self.instructions:
                self.p1_solution += 1
                if step == 'L':
                    next_node = self.nodes[current_node][0]
                else:
                    next_node = self.nodes[current_node][1]
                current_node = next_node
                if current_node == 'ZZZ':
                    break
                next_node = None
            
        return True

    def p2(self):
        self.nodes = {}
        self.distances = []
        self.instructions = []
        self.current_nodes = []
        self.next_nodes = []
        self.p2_solution = 0
        for char in self.input_list[0]:
                self.instructions.append(char)
        for line in self.input_list:
            if '=' in line:
                readline = re.match(r"^(?P<node>...) = \((?P<left>...), (?P<right>...)\)",line)
                self.nodes[readline.group('node')] = [readline.group('left'), readline.group('right')]
                if readline.group('node')[2] == 'A':
                    self.current_nodes.append(readline.group('node'))
                
        for node in self.current_nodes: # For each potential starting node
            current_node = node
            next_node = None
            distance = 0 # start with distance 0 and lets find the distance to a Z.
            step_cycle = itertools.cycle(self.instructions) 
            for step in step_cycle:
                distance += 1
                
                if step == 'L': # if the step is L... 
                    next_node = self.nodes[current_node][0] # find the next L step
                    if next_node[2] == 'Z':
                        self.distances.append(distance)
                        break
                if step == 'R': # if the step is R... 
                    next_node = self.nodes[current_node][1] # find the next L step
                    if next_node[2] == 'Z':
                        self.distances.append(distance)
                        break

                current_node = next_node
                next_node = None
        pass
        self.p2_solution = math.lcm(*self.distances)
        return True

def main():
    parser = argparse.ArgumentParser(description=f'AOC2023 Puzzle Day { DAY }')
    parser.add_argument("-p", "--showpuzzle", help="Display Puzzle Text", action='store_true')
    parser.add_argument("-s", "--showsample", help="Display Sample Input", action='store_true')
    args = parser.parse_args()
    
    if args.showpuzzle:
        print(f"###############\nAOC 2023 DAY {DAY} PUZZLE TEXT\n###############")
        print(PUZZLE_TEXT)
    
    if args.showsample:
        print(f"###############\nAOC 2023 DAY {DAY} P1 SAMPLE INPUT\n###############")
        print(P1_SAMPLE_INPUT.strip())
        print(f"###############\nAOC 2023 DAY {DAY} P1 SAMPLE INPUT\n###############")
        print(P2_SAMPLE_INPUT.strip())
        print(f"\n###############\nAOC 2023 DAY {DAY} P1 SAMPLE SOLUTION\n###############")
        print(P1_SAMPLE_SOLUTION)
        print(f"\n###############\nAOC 2023 DAY {DAY} P2 SAMPLE SOLUTION\n###############")
        print(P2_SAMPLE_SOLUTION)
    

    if P1_SAMPLE_SOLUTION:            
        print("PART 1\nTesting Sample...\n")
        start_time = time()
        sample = Puzzle(input_text=P1_SAMPLE_INPUT)
        sample.p1()
        if P1_SAMPLE_SOLUTION == sample.p1_solution:
            print("Sample correct.")
        else:
            print(f"Sample failed; Expected {P1_SAMPLE_SOLUTION}, got {sample.p1_solution}")
        print(f"Elapsed time {elapsed_time(start_time)}")
        if PUZZLE_INPUT:
            puzzle = Puzzle(input_text=PUZZLE_INPUT)
            puzzle.p1()
            print("Processing Input...\n")
            start_time = time()
            print(f'SOLUTION: {puzzle.p1_solution}')
            print(f"Elapsed time {elapsed_time(start_time)}")
        
    if P2_SAMPLE_SOLUTION:
        print("PART 2\nTesting Sample...\n")
        start_time = time()
        sample = Puzzle(input_text=P2_SAMPLE_INPUT)
        sample.p2()
        if P2_SAMPLE_SOLUTION == sample.p2_solution:
            print("Sample correct.")
        else:
            print(f"Sample failed; Expected {P2_SAMPLE_SOLUTION}, got {sample.p2_solution}")
        print(f"Elapsed time {elapsed_time(start_time)}")
        if PUZZLE_INPUT:
            print("Processing Input...\n")
            start_time = time()
            puzzle.p2()
            print(f'SOLUTION: {puzzle.p2_solution}')
            print(f"Elapsed time {elapsed_time(start_time)}")
    
if __name__ == "__main__":
    main()