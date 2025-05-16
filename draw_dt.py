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
BV="550"
# define histograms for delta T btw 2 channels (at cfd = 20%)

hdt_ch0_3 = ROOT.TH1F("hdt01", "Run5: CFD(20%) of Ch0 - Ch3 (MCP - K1 full-irrad) @ BV "+BV, 60, -5, 5)
hdt_ch0_4 = ROOT.TH1F("hdt02", "Run5: CFD(20%) of Ch0 - Ch4 (MCP - K1 half-irrad) @ BV "+BV, 60, -5, 5)
hdt_ch0_5 = ROOT.TH1F("hdt03", "Run5: CFD(20%) of Ch0 - Ch5 (MCP - HPK1) @ BV "+BV, 60, -5, 5)
hdt_ch0_6 = ROOT.TH1F("hdt04", "Run5: CFD(20%) of Ch0 - Ch6 (MCP - HPK2) @ BV "+BV, 60, -5, 5)
hdt_ch0_7 = ROOT.TH1F("hdt05", "Run5: CFD(20%) of Ch0 - Ch7 (MCP - HPK3) @ BV "+BV, 60, -5, 5)
#---
hdt_ch3_4 = ROOT.TH1F("hdt06", "Run5: CFD(20%) of Ch3 - Ch4 (K1 full-irrad - K1 half-irrad) @ BV "+BV, 60, -5, 5)
hdt_ch3_5 = ROOT.TH1F("hdt07", "Run5: CFD(20%) of Ch3 - Ch5 (K1 full-irrad - HPK1) @ BV "+BV, 60, -5, 5)
hdt_ch3_6 = ROOT.TH1F("hdt08", "Run5: CFD(20%) of Ch3 - Ch6 (K1 full-irrad - HPK2) @ BV "+BV, 60, -5, 5)
hdt_ch3_7 = ROOT.TH1F("hdt09", "Run5: CFD(20%) of Ch3 - Ch7 (K1 full-irrad - HPK3) @ BV "+BV, 60, -5, 5)
#---
hdt_ch4_5 = ROOT.TH1F("hdt10", "Run5: CFD(20%) of Ch4 - Ch5 (K1 half-irrad - HPK1) @ BV "+BV, 60, -5, 5)
hdt_ch4_6 = ROOT.TH1F("hdt11", "Run5: CFD(20%) of Ch4 - Ch6 (K1 half-irrad - HPK2) @ BV "+BV, 60, -5, 5)
hdt_ch4_7 = ROOT.TH1F("hdt12", "Run5: CFD(20%) of Ch4 - Ch6 (K1 half-irrad - HPK3) @ BV "+BV, 60, -5, 5)
#---
hdt_ch5_6 = ROOT.TH1F("hdt13", "Run5: CFD(20%) of Ch5 - Ch6 (HPK1 - HPK2) @ BV "+BV, 60, -5, 5)
hdt_ch5_7 = ROOT.TH1F("hdt14", "Run5: CFD(20%) of Ch5 - Ch7 (HPK1 - HPK3) @ BV "+BV, 60, -5, 5)
#---
hdt_ch6_7 = ROOT.TH1F("hdt15", "Run5: CFD(20%) of Ch6 - Ch7 (HPK2 - HPK3) @ BV "+BV, 60, -5, 5)


# hist list
hists = {
        "Ch0-3: MCP - K1_fullIR":       (hdt_ch0_3, ROOT.kBlack),
        "Ch0-4: MCP - K1_halfIR":       (hdt_ch0_4, ROOT.kBlack),
        "Ch0-5: MCP - HPK1":            (hdt_ch0_5, ROOT.kBlack),
        "Ch0-6: MCP - HPK2":            (hdt_ch0_6, ROOT.kBlack),
        "Ch0-7: MCP - HPK3":            (hdt_ch0_7, ROOT.kBlack),
        "Ch3-4: K1_fullIR - K1_halfIR": (hdt_ch3_4, ROOT.kBlue),
        "Ch3-5: K1_fullIR - HPK1":      (hdt_ch3_5, ROOT.kBlue),
        "Ch3-6: K1_fullIR - HPK2":      (hdt_ch3_6, ROOT.kBlue),
        "Ch3-7: K1_fullIR - HPK3":      (hdt_ch3_7, ROOT.kBlue),
        "Ch4-5: K1_halfIR - HPK1":      (hdt_ch4_5, ROOT.kYellow+2),
        "Ch4-6: K1_halfIR - HPK2":      (hdt_ch4_6, ROOT.kYellow+2),
        "Ch4-7: K1_halfIR - HPK3":      (hdt_ch4_7, ROOT.kYellow+2),
        "Ch5-6: HPK1 - HPK2":           (hdt_ch5_6, ROOT.kOrange+7),
        "Ch5-7: HPK1 - HPK3":           (hdt_ch5_7, ROOT.kOrange+7),
        "Ch6-7: HPK2 - HPK3":           (hdt_ch6_7, ROOT.kOrange+2),
}

#event loop  
# fill histogram with dT using cdf[channel][ 0(=10%), *1(=20%)*, .. 6(=70%)]
for event in tree:
    if len(event.pmax) > 5 and (event.pmax_fit[4] > 5):
        hdt_ch0_3.Fill((event.cfd[0][1] - event.cfd[3][1])) #dt MCP - K1full
        hdt_ch0_4.Fill((event.cfd[0][1] - event.cfd[4][1])) #dt MCP - K1half
        hdt_ch0_5.Fill((event.cfd[0][1] - event.cfd[5][1])) #dt MCP - HPK1
        hdt_ch0_6.Fill((event.cfd[0][1] - event.cfd[6][1])) #dt MCP - HPK2
        hdt_ch0_7.Fill((event.cfd[0][1] - event.cfd[7][1])) #dt MCP - HPK3
        hdt_ch3_4.Fill((event.cfd[3][1] - event.cfd[4][1])) #dt K1full - K1half
        hdt_ch3_5.Fill((event.cfd[3][1] - event.cfd[5][1])) #dt K1full - HPK1
        hdt_ch3_6.Fill((event.cfd[3][1] - event.cfd[6][1])) #dt K1full - HPK2
        hdt_ch3_7.Fill((event.cfd[3][1] - event.cfd[7][1])) #dt K1full - HPK3
        hdt_ch4_5.Fill((event.cfd[4][1] - event.cfd[5][1])) #dt K1half - HPK1
        hdt_ch4_6.Fill((event.cfd[4][1] - event.cfd[6][1])) #dt K1half - HPK2
        hdt_ch4_7.Fill((event.cfd[4][1] - event.cfd[7][1])) #dt K1half - HPK3
        hdt_ch5_6.Fill((event.cfd[5][1] - event.cfd[6][1])) #dt HPK1 - HPK2
        hdt_ch5_7.Fill((event.cfd[5][1] - event.cfd[7][1])) #dt HPK1 - HPK3
        hdt_ch6_7.Fill((event.cfd[6][1] - event.cfd[7][1])) #dt HPK2 - HPK3

ROOT.gStyle.SetOptStat(111111)

# Canvas1: draw 4 area_new with different pmax cuts
c1 = ROOT.TCanvas("c1", "c1", 2000, 1500)
c1.Divide(5,3)
c1.SetLogy()
legends ={}
for i, (label, (hist, color)) in enumerate(hists.items()):
    c1.cd(i+1)
    hist.SetLineColor(color)

    # Gaussian fit in range (@ypark please change this range!!)
    fit = ROOT.TF1(f"gaus_{label}", "gaus", -5, 5)  # fit range
    hist.Fit(fit, "RQ")  # R = fit within defined range, Q = quiet
    mean = fit.GetParameter(1)   # mean of Gaussian
    sigma = fit.GetParameter(2)  # sigma of Gaussian

    hist.GetXaxis().SetTitle("#delta T (ns)")
    hist.GetYaxis().SetTitle("Events")
    hist.GetXaxis().SetTitleSize(0.045)
    hist.GetYaxis().SetTitleSize(0.045)
    hist.Draw("hist same")

    legend = ROOT.TLegend(0.1, 0.75, 0.4, 0.88)
    legend.SetBorderSize(0)
    legend.SetTextSize(0.05)
    legend.AddEntry(hist, f"{label}, #mu = {mean:.2f}, #sigma = {sigma:.2f}", "l")
    legend.AddEntry(0, f"#mu = {mean:.2f}", "l")
    legend.AddEntry(0, f"#sigma = {sigma:.2f}", "l")
    legend.Draw()
    legends[label] = legend

c1.Update()
c1.SaveAs("hdT_bv-"+BV+"_allchannels.png")
