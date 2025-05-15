import ROOT

# Run5 for K1 analysis (BV @ 450, 500, 525, 550V)
#file = ROOT.TFile.Open("../stats_Sr_Run5_Ch0-450V_Ch1-450V_Ch3-140V_trig5V.root")
#file = ROOT.TFile.Open("../stats_Sr_Run5_Ch0-500V_Ch1-500V_Ch3-200V_trig5V.root")
#file = ROOT.TFile.Open("../stats_Sr_Run5_Ch0-525V_Ch1-525V_Ch3-180V_trig5V.root")
#file = ROOT.TFile.Open("../stats_Sr_Run5_Ch0-550V_Ch1-550V_Ch3-160V_trig5V.root")
file = ROOT.TFile.Open("../stats_Sr_Run6_Ch0-610V_Ch1-590V_Ch3-190V_trig5V.root")
tree = file.Get("Analysis")

# set Bias Voltage (string type)
BV="590"

# histograms for different pmax[4] cut thresholds
hists = {
    "ch-0 pmax": ROOT.TH1F("hpmax0", "pmax_fit in ch-0 MCP Trig @BV"+BV, 100, 0, 800),
    "ch-1 pmax": ROOT.TH1F("hpmax1", "pmax_fit in ch-1 No K2 @BV"+BV, 100, 0, 400),
    "ch-2 pmax": ROOT.TH1F("hpmax2", "pmax_fit in ch-2 No K2 @BV"+BV, 100, 0, 400),
    "ch-3 pmax": ROOT.TH1F("hpmax3", "pmax_fit in ch-3 K1 full-irrad @BV"+BV, 100, 0, 400),
    "ch-4 pmax": ROOT.TH1F("hpmax4", "pmax_fit in ch-4 K1 half-irrad @BV"+BV, 100, 0, 400),
    "ch-5 pmax": ROOT.TH1F("hpmax5", "pmax_fit in ch-5 HPK 1 @BV"+BV, 100, 0, 400),
    "ch-6 pmax": ROOT.TH1F("hpmax6", "pmax_fit in ch-6 HPK 2 @BV"+BV, 100, 0, 400),
    "ch-7 pmax": ROOT.TH1F("hpmax7", "pmax_fit in ch-7 HPK 3 @BV"+BV, 100, 0, 400),
}

# set pmaxCut for every channel (int type)
pmaxCut = 18

for event in tree:
    for i in range(8):
        if(event.pmax_fit[i] > pmaxCut):
              hists[f"ch-{i} pmax"].Fill(event.pmax_fit[i])

colors = {
    "ch-0 pmax": ROOT.kGreen+2,  # Trigger MCP
    "ch-1 pmax": ROOT.kBlue,     # no K2
    "ch-2 pmax": ROOT.kBlue,     # no K2
    "ch-3 pmax": ROOT.kRed,      # K1 full-irrad
    "ch-4 pmax": ROOT.kRed,      # K1 half-irrad
    "ch-5 pmax": ROOT.kYellow+1, # HPK1
    "ch-6 pmax": ROOT.kYellow+1, # HPK2
    "ch-7 pmax": ROOT.kYellow+1, # HPK3
}

ROOT.gStyle.SetOptStat(111111)

# Canvas1: draw 4 area_new with different pmax cuts
c1 = ROOT.TCanvas("c1", "c1", 1600, 800)
c1.Divide(4,2)

legends ={}

for i, (label, hist) in enumerate(hists.items()):
    pad = c1.cd(i+1)
    pad.SetLogy()
    hist.SetLineColor(colors[label])
    hist.GetXaxis().SetTitle("p_{max} from gaus fit (mV)")
    hist.GetYaxis().SetTitle("Events")
    hist.GetXaxis().SetTitleSize(0.045)
    hist.GetYaxis().SetTitleSize(0.045)
    hist.Draw("hist")

    peak_bin = hist.GetMaximumBin()
    peak_value = hist.GetXaxis().GetBinCenter(peak_bin)
    print(f"{label}: {peak_value:.1f}")

    legend = ROOT.TLegend(0.4, 0.6, 0.88, 0.7)
    legend.SetBorderSize(0)
    legend.SetTextSize(0.04)
    legend.AddEntry(hist, f"{label}, peak = {peak_value:.1f}", "l")
    legend.Draw()
    legends[label] = legend

c1.Update()
c1.SaveAs(f"hRun5_all_pmax_fit_cut-{pmaxCut}_bv-"+BV+".png")
