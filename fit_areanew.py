import ROOT

# Run5 for K1 analysis (BV @ 550V)
file = ROOT.TFile.Open("../stats_Sr_Run5_Ch0-550V_Ch1-550V_Ch3-160V_trig5V.root")
#file = ROOT.TFile.Open("../stats_Sr_Run5_Ch0-500V_Ch1-500V_Ch3-200V_trig5V.root")
#file = ROOT.TFile.Open("../stats_Sr_Run5_Ch0-500V_Ch1-500V_Ch3-200V_trig5V.root")
tree = file.Get("Analysis")
BV="550"

# histograms for different pmax[4] cut thresholds
hists = {
    "pmax > 10": ROOT.TH1F("h_cut10", "K1 (half-irrad) area_new BV 550 & pmax > 10", 100, 0, 150),
    "pmax > 15": ROOT.TH1F("h_cut15", "K1 (half-irrad) area_new BV 550 & pmax > 15", 100, 0, 200),
    "pmax > 18": ROOT.TH1F("h_cut18", "K1 (half-irrad) area_new BV 550 & pmax > 18", 100, 0, 200),
    "pmax > 20": ROOT.TH1F("h_cut20", "K1 (half-irrad) area_new BV 550 & pmax > 20", 100, 0, 200),
}

for event in tree:
    if len(event.pmax) > 4 and len(event.area_new) > 4:
        val = event.area_new[4]
        if event.pmax[4] > 10:
            hists["pmax > 10"].Fill(val)
        if event.pmax[4] > 15:
            hists["pmax > 15"].Fill(val)
        if event.pmax[4] > 18:
            hists["pmax > 18"].Fill(val)
        if event.pmax[4] > 20:
            hists["pmax > 20"].Fill(val)

colors = {
    "pmax > 10": ROOT.kGreen+2,
    "pmax > 15": ROOT.kYellow+1,
    "pmax > 18": ROOT.kBlue,
    "pmax > 20": ROOT.kBlack,
}

ROOT.gStyle.SetOptStat(0)

# Canvas1: draw 4 area_new with different pmax cuts
c1 = ROOT.TCanvas("c1", "c1", 800, 700)
c1.Divide(2,2)
c1.SetLogy()

legends ={}

for i, (label, hist) in enumerate(hists.items()):
    c1.cd(i+1)
    hist.SetLineColor(colors[label])
    hist.GetXaxis().SetTitle("Area_{new} = Q #times R_{Imp} (fC #times k#Omega)")
    hist.GetYaxis().SetTitle("Events")
    hist.GetXaxis().SetTitleSize(0.045)
    hist.GetYaxis().SetTitleSize(0.045)
    hist.Draw("hist same")

    peak_bin = hist.GetMaximumBin()
    peak_value = hist.GetXaxis().GetBinCenter(peak_bin)
    print(f"{label}: peak at area_new[4] = {peak_value:.3f}")

    legend = ROOT.TLegend(0.3, 0.75, 0.88, 0.88)
    legend.SetBorderSize(0)
    legend.SetTextSize(0.05)
    legend.AddEntry(hist, f"{label}, peak = {peak_value:.3f}", "l")
    legend.Draw()
    legends[label] = legend

c1.Update()
c1.SaveAs("hRun5_area_new_K1_half-irrad_bv-550_pmaxcut-5-25.png")

# Canvas 2: With extracted MPV & Q collection by Landau fitting
c2 = ROOT.TCanvas("c2", "c2", 800, 700)
c2.Divide(2,2)
c2.SetLogy()
print(f"Bias Voltage={BV}")

for i, (label, hist) in enumerate(hists.items()):
    c2.cd(i+1)
    hist.SetLineColor(colors[label])
    hist.SetLineWidth(2)
    fit = ROOT.TF1(f"landau_{label}", "landau", 0, 100)
    hist.Fit(fit, "RQ")  # "R" for range, "Q" for quiet mode

    mpv = fit.GetParameter(1)  # Landau: [0]=norm, [1]=MPV, [2]=sigma
    print(f"{label}: MPV = {mpv:.3f}, MPV/4.7 = Q_collection = {mpv/4.7:.3f}")
    hist.Draw("same")

    legend = ROOT.TLegend(0.22, 0.7, 0.88, 0.88)
    legend.SetBorderSize(0)
    legend.SetFillStyle(0)
    legend.SetTextSize(0.054)
    legend.AddEntry(hist, f"{label}, MPV = {mpv:.3f}", "l")
    legend.AddEntry(0, f"#it{{Q}}_{{Collection}}(=MPV/4.7) = {mpv/4.7:.3f}", "")
    legends[label] = legend
    legend.Draw()

c2.Update()
c2.SaveAs("hRun5_MPV_area_new_K1_half-irrad_bv-550_pmaxcut-5-25.png")

