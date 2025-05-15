import ROOT

# K1 half irrad data at BV=500, 550V
file = ROOT.TFile.Open("stats_Sr_Run5_Ch0-500V_Ch1-500V_Ch3-200V_trig5V.root")
tree = file.Get("Analysis")

hareanew = ROOT.TH1F("h_area_new", "Run5: Area of half-irrad K1 @ BV 500", 200, 0, 200)
harea    = ROOT.TH1F("h_area", "Run5: Area of half-irrad K1 @ BV 500", 200, 0, 200)
hareanc  = ROOT.TH1F("h_area_nc", "", 200, 0, 200)
hareawin = ROOT.TH1F("h_area_win", "", 200, 0, 200)
harea_diff1 = ROOT.TH1F("harea_diff1", "Run5: half-irrad K1 @ BV 500", 200, -1.5, 1.5)
harea_diff2 = ROOT.TH1F("harea_diff2", "Run5: half-irrad K1 @ BV 500", 200, -1.5, 1.5)
harea_diff3 = ROOT.TH1F("harea_diff3", "Run5: half-irrad K1 @ BV 500", 200, -1.5, 1.5)

for event in tree:
    if len(event.area) > 4:
        hareanew.Fill(event.area_new[4])
        harea.Fill(event.area[4])
        hareanc.Fill(event.area_nc[4])
        hareawin.Fill(event.area_fixed_window[4])
        harea_diff1.Fill((event.area_new[4] - event.area[4])/event.area_new[4])
        harea_diff2.Fill((event.area_new[4] - event.area_nc[4])/event.area_new[4])
        harea_diff3.Fill((event.area_new[4] - event.area_fixed_window[4])/event.area_new[4])

ROOT.gStyle.SetOptStat(0)

#canvas1: area[4] vs. area_new[4]
c1 = ROOT.TCanvas("c1", "c1", 800, 700)
c1.SetLogy()

harea.SetLineColor(ROOT.kBlack)
hareanew.SetLineColor(ROOT.kRed)
hareanc.SetLineColor(ROOT.kBlue)
hareawin.SetLineColor(ROOT.kGreen)

harea.GetXaxis().SetTitle("Integrated Area")
harea.GetYaxis().SetTitle("Events")
harea.GetXaxis().SetTitleSize(0.04)
harea.GetYaxis().SetTitleSize(0.04)
harea.Draw("hist")
hareanc.Draw("hist same")
hareawin.Draw("hist same")
hareanew.Draw("hist same")

legend = ROOT.TLegend(0.3, 0.66, 0.88, 0.88)
legend.SetBorderSize(0)
legend.SetTextSize(0.03)
legend.AddEntry(hareanew, "area_new K1 half-irrad @ 500V", "l")
legend.AddEntry(harea, "area K1 half-irrad @ 500V", "l")
legend.AddEntry(hareanc, "area_nc K1 half-irrad @ 500V", "l")
legend.AddEntry(hareawin, "area_fixed_window K1 half-irrad @ 500V", "l")
legend.Draw()

c1.Update()
c1.SaveAs("hRun5_area_vs_areanew_K1_half-irrad_bv-500.png")


#canvas2: (area[4]-pmad_new[4]) / area[4]

c2 = ROOT.TCanvas("c2", "c2", 800, 700)
c2.SetLogy()
#ROOT.gStyle.SetOptStat(1111111)

harea_diff1.SetLineColor(ROOT.kBlack)
harea_diff2.SetLineColor(ROOT.kBlue)
harea_diff3.SetLineColor(ROOT.kGreen)

harea_diff2.GetXaxis().SetTitle("(area_new - area)/area_new")
harea_diff2.GetYaxis().SetTitle("Events")
harea_diff2.GetXaxis().SetTitleSize(0.04)
harea_diff2.GetYaxis().SetTitleSize(0.035)
harea_diff2.Draw("hist")
harea_diff1.Draw("hist same")
harea_diff3.Draw("hist same")

leg = ROOT.TLegend(0.15, 0.65, 0.48, 0.88)
leg.SetBorderSize(0)
leg.SetTextSize(0.03)
leg.AddEntry(harea_diff1, "area_new - area", "l")
leg.AddEntry(harea_diff2, "area_new - area_nc", "l")
leg.AddEntry(harea_diff3, "area_new - area_fixed_window", "l")
leg.Draw()

c2.Update()
c2.SaveAs("hRun5_diff_area_vs_areanew_K1_half-irrad_bv-500.png")

