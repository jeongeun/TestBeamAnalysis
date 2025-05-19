import ROOT
import math

# Run0
#file = ROOT.TFile.Open("../stats_Sr_Run0_Ch0-500V_Ch1-500V_Ch2-300V_Ch3-180V_trig5V.root")
# Run1
#file = ROOT.TFile.Open("../stats_Sr_Run1_Ch0-500V_Ch1-500V_Ch2-300V_Ch3-120V_trig5V.root")
#file = ROOT.TFile.Open("../stats_Sr_Run1_Ch0-500V_Ch1-500V_Ch2-300V_Ch3-140V_trig5V.root")
#file = ROOT.TFile.Open("../stats_Sr_Run1_Ch0-500V_Ch1-500V_Ch2-300V_Ch3-160V_trig5V.root")
#file = ROOT.TFile.Open("../stats_Sr_Run1_Ch0-500V_Ch1-500V_Ch2-300V_Ch3-180V_trig5V.root")
#file = ROOT.TFile.Open("../stats_Sr_Run1_Ch0-500V_Ch1-500V_Ch2-300V_Ch3-190V_trig5V.root")
#file = ROOT.TFile.Open("../stats_Sr_Run1_Ch0-500V_Ch1-500V_Ch2-300V_Ch3-200V_trig5V.root")
# Run2
#file = ROOT.TFile.Open("../stats_Sr_Run2_Ch0-550V_Ch1-550V_Ch2-275V_Ch3-100V_trig5V.root")
#file = ROOT.TFile.Open("../stats_Sr_Run2_Ch0-550V_Ch1-550V_Ch2-300V_Ch3-100V_trig5V.root")
file = ROOT.TFile.Open("../stats_Sr_Run2_Ch0-550V_Ch1-550V_Ch2-320V_Ch3-100V_trig5V.root")
# Run3
#file = ROOT.TFile.Open("../stats_Sr_Run3_Ch0-550V_Ch1-550V_Ch2-320V_Ch3-100V_trig5V.root")
# Run4
#file = ROOT.TFile.Open("../stats_Sr_Run4_Ch0-550V_Ch1-550V_Ch2-200V_Ch3-100V_trig5V.root")
#file = ROOT.TFile.Open("../stats_Sr_Run4_Ch0-550V_Ch1-550V_Ch2-250V_Ch3-100V_trig5V.root")
#file = ROOT.TFile.Open("../stats_Sr_Run4_Ch0-550V_Ch1-550V_Ch2-310V_Ch3-100V_trig5V.root")
# Run5
#file = ROOT.TFile.Open("../stats_Sr_Run5_Ch0-450V_Ch1-450V_Ch3-140V_trig5V.root")
#file = ROOT.TFile.Open("../stats_Sr_Run5_Ch0-500V_Ch1-500V_Ch3-200V_trig5V.root")
#file = ROOT.TFile.Open("../stats_Sr_Run5_Ch0-525V_Ch1-525V_Ch3-180V_trig5V.root")
#file = ROOT.TFile.Open("../stats_Sr_Run5_Ch0-550V_Ch1-550V_Ch3-160V_trig5V.root")
# Run6
#file = ROOT.TFile.Open("../stats_Sr_Run6_Ch0-610V_Ch1-590V_Ch3-190V_trig5V.root")

# Load file and tree
tree = file.Get("Analysis")
BV = "K2-320"
pmaxCut = 25

labels = {0: "Trig", 1: "K2_1", 2: "K2_2", 3: "K1 full-irrad"}
color_map = {0: ROOT.kGreen+2, 1: ROOT.kBlue, 2: ROOT.kBlue+9}
channel_pairs = [(i, j) for i in range(3) for j in range(i+1, 3)]
# Histogram container
hists = {}

# Create histograms dynamically
for i, j in channel_pairs:
    name = f"hdt{i}{j}"
    title = f"SPS-MAY-2025: dT(Ch{i}-{j}) @ BV {BV}, pmaxCut>{pmaxCut}"
    hist= ROOT.TH1F(name, title, 90, -1., 1.)
    hist.SetLineColor(color_map[i])
    hists[(i, j)] = hist

count_total = 0
count_passed = 0
# Event loop

for event in tree:
    count_total += 1
    for i in range(3):
        if event.pmax_fit[i] > pmaxCut:
            count_passed += 1
            for i, j in channel_pairs:
                dt = event.cfd[i][1] - event.cfd[j][1]
                hists[(i, j)].Fill(dt)
            
            #for (i, j), (hist, _) in hists.items():
            #    dt = event.cfd[i][1] - event.cfd[j][1]
            #    hist.Fill(dt)

ROOT.gStyle.SetOptStat(111111)
print(f"Total events: {count_total}, Passed filter: {count_passed}")

# Canvas Draw and Fitting

for i_ref in range(3):
    # extract (i,j) list for each i
    pairs_for_i = [(i, j) for (i, j) in hists if i == i_ref]
    canvas = ROOT.TCanvas(f"c{i_ref}", f"Channel {i_ref} reference", 2000, 1200)
    canvas.Divide(2, (len(pairs_for_i) + 1) // 2)

    for idx, (i, j) in enumerate(pairs_for_i):
        hist = hists[(i, j)]
        pad = canvas.cd(idx + 1)
        hist.SetLineColor(color_map[i])
        # Label styling
        hist.GetXaxis().SetTitle("#Deltat (ns)")
        hist.GetYaxis().SetTitle("Events")
        hist.GetXaxis().SetTitleSize(0.045)
        hist.GetYaxis().SetTitleSize(0.045)
        hist.SetMinimum(0)
        hist.Draw("hist")

        # Gaussian fit
        fit = ROOT.TF1(f"gaus_{i}_{j}", "gaus", -1, 1)
        fit.SetLineColor(ROOT.kRed)
        fit.SetLineWidth(2)
        fit_result = hist.Fit(fit, "SRQ")

        mean = sigma = float("nan")

        if hasattr(fit_result, 'IsValid') and fit_result.IsValid():
            try:
                mean = fit.GetParameter(1)
                sigma = fit.GetParameter(2)
            except Exception as e:
                print(f"[FitParamError] {hist.GetName()} fit exists but parameter access failed: {e}")
        fit.Draw("same")

        y_max = hist.GetMaximum()
        #line1 = ROOT.TLine(mean - sigma, 0, mean - sigma, y_max)
        #line2 = ROOT.TLine(mean + sigma, 0, mean + sigma, y_max)
        #for line in (line1, line2):
        #    line.SetLineStyle(2)
        #    line.SetLineColor(ROOT.kBlue+3)
        #    line.Draw("same")

        y1 = fit.Eval(mean - sigma)
        y2 = fit.Eval(mean + sigma)
        hline = ROOT.TLine(mean - sigma, y1, mean + sigma, y2)
        hline.SetLineStyle(2)
        hline.SetLineColor(ROOT.kRed+3)
        hline.Draw("same")
        # Legend
        legend = ROOT.TLegend(0.52, 0.4, 0.88, 0.65)
        legend.SetBorderSize(0)
        legend.SetTextSize(0.038)
        legend.AddEntry(hist, f"#Deltat(Ch{i} - Ch{j})", "l")
        legend.AddEntry(fit, f"fit: #mu = {mean*1000:.2f} ps", "l")
        legend.AddEntry(hline, f"#sigma{i}{j} = {sigma*1000:.2f} ps", "l")
        legend.AddEntry(0, f"t_{{resol}} = {sigma*1000/math.sqrt(2):.2f} ps", "l")
        legend.Draw()

#        legends.append(legend)
        pad.Modified()
        pad.Update()

        print(f"K-2 BV {BV} with pmaxCut > {pmaxCut} in Ch{i} - Ch{j} -------")
        print(f"mean= {mean*1000:.3f} ps, sigma_{i}{j} = {sigma*1000:.3f}, time resolution = {sigma*1000/math.sqrt(2):.3f} ps")

    canvas.Update()
    canvas.SaveAs(f"hdt_BV{BV}_Ch{i_ref}_ptcut{pmaxCut}_comparisons.png")
