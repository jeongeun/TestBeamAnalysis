import ROOT

file = ROOT.TFile.Open("stats_Sr_Run2_Ch0-550V_Ch1-550V_Ch2-320V_Ch3-100V_trig5V.root")
#file = ROOT.TFile.Open("stats_Sr_Run3_Ch0-550V_Ch1-550V_Ch2-320V_Ch3-100V_trig5V.root")
#file = ROOT.TFile.Open("stats_Sr_Run4_Ch0-550V_Ch1-550V_Ch2-310V_Ch3-100V_trig5V.root")
#file = ROOT.TFile.Open("stats_Sr_Run5_Ch0-550V_Ch1-550V_Ch3-160V_trig5V.root")
tree = file.Get("Analysis")

hpmax = ROOT.TH1F("h_pmax", "Run2: Vmax of half-irrad K1 @ BV 550", 200, 0, 800)
hpmaxfit = ROOT.TH1F("h_pmax_fit", "", 200, 0, 800)
hpmax_diff = ROOT.TH1F("hpmax_diff", "Run2: half-irrad K1 @ BV 550", 100, -0.5, 0.5)

for event in tree:
    if len(event.pmax) > 4:
        hpmax.Fill(event.pmax[4])
        hpmaxfit.Fill(event.pmax_fit[4])
        hpmax_diff.Fill((event.pmax[4] - event.pmax_fit[4])/event.pmax[4])

ROOT.gStyle.SetOptStat(0)

#canvas1: pmax[4] vs. pmad_fit[4]
c1 = ROOT.TCanvas("c1", "c1", 800, 700)
c1.SetLogy()

hpmax.SetLineColor(ROOT.kBlack)
hpmaxfit.SetLineColor(ROOT.kBlue)

hpmax.GetXaxis().SetTitle("Vmax (mV)")
hpmax.GetYaxis().SetTitle("Events / (4 mV)")
hpmax.GetXaxis().SetTitleSize(0.04)
hpmax.GetYaxis().SetTitleSize(0.04)
hpmax.Draw("hist")
hpmaxfit.Draw("hist same")

legend = ROOT.TLegend(0.35, 0.66, 0.88, 0.88)
legend.SetBorderSize(0)
legend.SetTextSize(0.03)
legend.AddEntry(hpmax, "Nominal Vmax K1 half-irrad @ 550V", "l")
legend.AddEntry(hpmaxfit, "Gaus fit Vmax K1 half-irrad @ 550V", "l")
legend.Draw()

c1.Update()
c1.SaveAs("hRun2_pmax_vs_pmaxfit_K1_half-irrad_bv-550_pmaxcut-0.png")


#canvas2: (pmax[4]-pmad_fit[4]) / pmax[4]

c2 = ROOT.TCanvas("c2", "c2", 800, 700)
c2.SetLogy()
ROOT.gStyle.SetOptStat(1111111)

hpmax_diff.SetLineColor(ROOT.kBlack)

hpmax_diff.GetXaxis().SetTitle("(pmax - pmax_fit)/pmax")
hpmax_diff.GetYaxis().SetTitle("Events")
hpmax_diff.GetXaxis().SetTitleSize(0.04)
hpmax_diff.GetYaxis().SetTitleSize(0.035)
hpmax_diff.Draw("hist")

c2.Update()
c2.SaveAs("hRun2_diff_pmax_vs_pmaxfit_K1_half-irrad_bv-550_pmaxcut-0.png")

