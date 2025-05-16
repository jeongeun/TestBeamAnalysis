import ROOT

#file = ROOT.TFile.Open("../stats_Sr_Run0_Ch0-500V_Ch1-500V_Ch2-300V_Ch3-180V_trig5V.root")
#file = ROOT.TFile.Open("../stats_Sr_Run1_Ch0-500V_Ch1-500V_Ch2-300V_Ch3-120V_trig5V.root")
#file = ROOT.TFile.Open("../stats_Sr_Run1_Ch0-500V_Ch1-500V_Ch2-300V_Ch3-140V_trig5V.root")
#file = ROOT.TFile.Open("../stats_Sr_Run1_Ch0-500V_Ch1-500V_Ch2-300V_Ch3-160V_trig5V.root")
#file = ROOT.TFile.Open("../stats_Sr_Run1_Ch0-500V_Ch1-500V_Ch2-300V_Ch3-180V_trig5V.root")
#file = ROOT.TFile.Open("../stats_Sr_Run1_Ch0-500V_Ch1-500V_Ch2-300V_Ch3-190V_trig5V.root")
#file = ROOT.TFile.Open("../stats_Sr_Run1_Ch0-500V_Ch1-500V_Ch2-300V_Ch3-200V_trig5V.root")
#file = ROOT.TFile.Open("../stats_Sr_Run2_Ch0-550V_Ch1-550V_Ch2-275V_Ch3-100V_trig5V.root")
#file = ROOT.TFile.Open("../stats_Sr_Run2_Ch0-550V_Ch1-550V_Ch2-300V_Ch3-100V_trig5V.root")
#file = ROOT.TFile.Open("../stats_Sr_Run2_Ch0-550V_Ch1-550V_Ch2-320V_Ch3-100V_trig5V.root")
#file = ROOT.TFile.Open("../stats_Sr_Run3_Ch0-550V_Ch1-550V_Ch2-320V_Ch3-100V_trig5V.root")
#file = ROOT.TFile.Open("../stats_Sr_Run4_Ch0-550V_Ch1-550V_Ch2-200V_Ch3-100V_trig5V.root")
#file = ROOT.TFile.Open("../stats_Sr_Run4_Ch0-550V_Ch1-550V_Ch2-250V_Ch3-100V_trig5V.root")
#file = ROOT.TFile.Open("../stats_Sr_Run4_Ch0-550V_Ch1-550V_Ch2-310V_Ch3-100V_trig5V.root")
#file = ROOT.TFile.Open("../stats_Sr_Run5_Ch0-450V_Ch1-450V_Ch3-140V_trig5V.root")
#file = ROOT.TFile.Open("../stats_Sr_Run5_Ch0-500V_Ch1-500V_Ch3-200V_trig5V.root")
#file = ROOT.TFile.Open("../stats_Sr_Run5_Ch0-525V_Ch1-525V_Ch3-180V_trig5V.root")
#file = ROOT.TFile.Open("../stats_Sr_Run5_Ch0-550V_Ch1-550V_Ch3-160V_trig5V.root")
#file = ROOT.TFile.Open("../stats_Sr_Run6_Ch0-610V_Ch1-590V_Ch3-190V_trig5V.root")

#file = ROOT.TFile.Open("../stats_Sr_Run2_Ch0-550V_Ch1-550V_Ch2-320V_Ch3-100V_trig5V.root")
#file = ROOT.TFile.Open("stats_Sr_Run3_Ch0-550V_Ch1-550V_Ch2-320V_Ch3-100V_trig5V.root")
#file = ROOT.TFile.Open("../stats_Sr_Run4_Ch0-550V_Ch1-550V_Ch2-310V_Ch3-100V_trig5V.root")
file = ROOT.TFile.Open("../stats_Sr_Run5_Ch0-550V_Ch1-550V_Ch3-160V_trig5V.root")
tree = file.Get("Analysis")

# define histograms
hcfd_ch0 = ROOT.TH1F("h_cfd1", "Run5: CFD(20%) of Ch-0 MCP trigger @ BV 550", 200, -30, 30)
hcfd_ch3 = ROOT.TH1F("h_cfd2", "Run5: CFD(20%) of Ch-3 full-irrad K1 @ BV 550", 200, -30, 30)
hcfd_ch4 = ROOT.TH1F("h_cfd3", "Run5: CFD(20%) of Ch-4 half-irrad K1 @ BV 550", 200, -30, 30)
hcfd_ch5 = ROOT.TH1F("h_cfd4", "Run5: CFD(20%) of Ch-5 HPK 1 @ BV 550", 200, -30, 30)
hcfd_ch6 = ROOT.TH1F("h_cfd5", "Run5: CFD(20%) of Ch-6 HPK 2 @ BV 550", 200, -30, 30)
hcfd_ch7 = ROOT.TH1F("h_cfd6", "Run5: CFD(20%) of Ch-7 HPK 3 @ BV 550", 200, -30, 30)

hdt_12 = ROOT.TH1F("h_dt12", "Run5: dt_12 = t(Ch-0) - t(Ch-4)  @ BV 550", 200, -10, 10)
hdt_13 = ROOT.TH1F("h_dt13", "Run5: dt_13 = t(Ch-0) - t(Ch-5)  @ BV 550", 200, -10, 10)
hdt_23 = ROOT.TH1F("h_dt23", "Run5: dt_23 = t(Ch-4) - t(Ch-5)  @ BV 550", 200, -10, 10)

# hist list
hcfd_list = [
    ("Ch-0 MCP",  hcfd_ch0, ROOT.kBlack),
    ("Ch-3 K1 full-irrad", hcfd_ch3, ROOT.kBlue),
    ("Ch-4 K1 half-irrad", hcfd_ch4, ROOT.kRed),
    ("Ch-5 HPK 1", hcfd_ch5, ROOT.kGreen+2),
    ("Ch-6 HPK 2", hcfd_ch6, ROOT.kMagenta),
    ("Ch-7 HPK 3", hcfd_ch7, ROOT.kOrange+7)
]

for event in tree:
    if len(event.pmax) > 5 and (event.pmax_fit[4] > 15):
        hcfd_ch0.Fill(event.cfd[0][1]) # Ch-1 MCP with cfd=20%
        hcfd_ch3.Fill(event.cfd[3][1]) # Ch-3 K1(full-irrad) with cfd=20%
        hcfd_ch4.Fill(event.cfd[4][1]) # Ch-4 K1(half-irrad) with cfd=20%
        hcfd_ch5.Fill(event.cfd[5][1]) # Ch-5 HPK with cfd=20%
        hcfd_ch6.Fill(event.cfd[6][1]) # Ch-6 HPK with cfd=20%
        hcfd_ch7.Fill(event.cfd[7][1]) # Ch-7 HPK with cfd=20%

        hdt_12.Fill((event.cfd[0][1] - event.cfd[4][1])) #time diff btw MCP - K1#2
        hdt_13.Fill((event.cfd[0][1] - event.cfd[5][1])) #time diff btw MCP - HPK#1
        hdt_23.Fill((event.cfd[4][1] - event.cfd[5][1])) #time diff btw K1#2 - HPK#1

ROOT.gStyle.SetOptStat(0)

#canvas1: hcfd of MCP, K1#2, and HPK#1
c1 = ROOT.TCanvas("c1", "c1", 800, 700)
c1.SetLogy()

hcfd_1_20.SetLineColor(ROOT.kGreen+2)
hcfd_2_20.SetLineColor(ROOT.kRed+3)
hcfd_3_20.SetLineColor(ROOT.kBlue+2)

hcfd_1_20.GetXaxis().SetTitle("Time (CFD 20%)")
hcfd_1_20.GetYaxis().SetTitle("Events")
hcfd_1_20.GetXaxis().SetTitleSize(0.04)
hcfd_1_20.GetYaxis().SetTitleSize(0.04)
hcfd_1_20.Draw("hist")
hcfd_2_20.Draw("hist same")
hcfd_3_20.Draw("hist same")

legend = ROOT.TLegend(0.5, 0.66, 0.88, 0.88)
legend.SetBorderSize(0)
legend.SetTextSize(0.02)
legend.AddEntry(hcfd_1_20, "Ch-0: MCP Timing @ 550V", "l")
legend.AddEntry(hcfd_2_20, "Ch-4: K1 half-irrad @ 550V", "l")
legend.AddEntry(hcfd_3_20, "Ch-5: HPK @ 550V", "l")
legend.Draw()

c1.Update()
c1.SaveAs("hRun5_timing_cfd20_bv550.png")


#canvas2: (pmax[4]-pmad_fit[4]) / pmax[4]

c2 = ROOT.TCanvas("c2", "c2", 800, 700)
c2.SetLogy()
#ROOT.gStyle.SetOptStat(1111111)

hdt_12.SetLineColor(ROOT.kBlack)
hdt_13.SetLineColor(ROOT.kBlue)
hdt_23.SetLineColor(ROOT.kRed)

hdt_12.GetXaxis().SetTitle("Time difference")
hdt_12.GetYaxis().SetTitle("Events")
hdt_12.GetXaxis().SetTitleSize(0.04)
hdt_12.GetYaxis().SetTitleSize(0.035)
hdt_12.Draw("hist")
hdt_13.Draw("hist same")
hdt_23.Draw("hist same")

c2.Update()
c2.SaveAs("hRun5_dT_bv550.png")
