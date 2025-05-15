import ROOT
from collections import Counter

#file = ROOT.TFile.Open("../stats_Sr_Run2_Ch0-550V_Ch1-550V_Ch2-320V_Ch3-100V_trig5V.root")
#file = ROOT.TFile.Open("../stats_Sr_Run3_Ch0-550V_Ch1-550V_Ch2-320V_Ch3-100V_trig5V.root")
#file = ROOT.TFile.Open("../stats_Sr_Run4_Ch0-550V_Ch1-550V_Ch2-310V_Ch3-100V_trig5V.root")
file = ROOT.TFile.Open("../stats_Sr_Run5_Ch0-550V_Ch1-550V_Ch3-160V_trig5V.root")

#file = ROOT.TFile.Open("../stats_Sr_Run0_Ch0-500V_Ch1-500V_Ch2-300V_Ch3-180V_trig5V.root")
tree = file.Get("Analysis")

#count_pmax0 = 0

pmax_indices = [0, 1, 2, 3, 4, 5, 6, 7]
pmax_counts = Counter()

for event in tree:
    for i in pmax_indices:
        if len(event.pmax) > i:
            pmax_counts[i] += 1

for i in pmax_indices:
    print(f"Total events with pmax[{i}] available: {pmax_counts[i]}")
