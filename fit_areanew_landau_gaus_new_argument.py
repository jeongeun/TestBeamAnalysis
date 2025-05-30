import ROOT
import argparse
import math

# ─── landaufun: Landau ⊗ Gaussian convolution ───────────────────────────
def landaufun(x, par):
    np = 100       # number of convolution steps
    sc = 5         # convolution range in Gaussian sigma
    mpshift = -0.22278298  # MP shift correction

    xx = x[0]
    sum = 0.0

    # Convolution integration limits
    xlow = xx - sc * par[3]
    xupp = xx + sc * par[3]
    step = (xupp - xlow) / np

    for i in range(1, np + 1):
        xi = xlow + (i - 0.5) * step
        landau_val = ROOT.TMath.Landau(xi, par[1] + mpshift * par[0], par[0]) / par[0]
        gauss_val = ROOT.TMath.Gaus(xx, xi, par[3])
        sum += landau_val * gauss_val

    return par[2] * step * sum


# ─── argparse setup ────────────────────────────────────────────
parser = argparse.ArgumentParser(description="Run Landau (Landau fit analysis on ROOT file with given parameters.")

parser.add_argument("filename", type=str, help="Input ROOT filename")
parser.add_argument("Ch", type=int, help="Channel number (e.g., 5 for HPK1, 6 for HPK2, 7 for HPK3)")
parser.add_argument("Sensor", type=str, help="Sensor name (e.g., HPK1, HPK2, HPK3)")
parser.add_argument("BV", type=str, help="Bias voltage (e.g., 200)")
parser.add_argument("pmaxCut", type=int, help="pmax threshold (e.g., 100)")
parser.add_argument("binning", type=int, help="Number of bins (e.g., 100)")
parser.add_argument("xmin", type=float, help="Histogram X-axis minimum")
parser.add_argument("xmax", type=float, help="Histogram X-axis maximum")
parser.add_argument("--altFit", action="store_true", help="Enable alternative Landau-Gaussian convolution fit")

args = parser.parse_args()

# ─── Assign arguments ──────────────────────────────────────────
filename  = args.filename
Ch        = args.Ch
Sensor    = args.Sensor
BV        = args.BV
pmaxCut   = args.pmaxCut
binning   = args.binning
xmin      = args.xmin
xmax      = args.xmax
altFit    = args.altFit
# ─── ROOT analysis ─────────────────────────────────────────────
file = ROOT.TFile.Open(filename)
tree = file.Get("Analysis")

# Create histogram
hist = ROOT.TH1F("h_cut", f"{Sensor} area_new BV{BV} & pmax > {pmaxCut}", binning, xmin, xmax)

for event in tree:
    if len(event.pmax_fit) > 6 and len(event.area_new) > 6:
        if event.pmax_fit[Ch] > pmaxCut:
            val = event.area_new[Ch]
            hist.Fill(val)

ROOT.gStyle.SetOptStat(0)

# Canvas1: draw area_new
c1 = ROOT.TCanvas("c1", "c1", 700, 600)
c1.SetLogy()
hist.SetLineColor(ROOT.kYellow+2)
hist.SetLineWidth(2)
hist.GetXaxis().SetTitle("Area_{new} = Q #times R_{Imp} [fC k#Omega]")
hist.GetYaxis().SetTitle("Events")
hist.GetYaxis().SetTitleOffset(1.0)
hist.GetXaxis().SetTitleSize(0.048)
hist.GetYaxis().SetTitleSize(0.047)
hist.Draw("hist")

# Find peak bin
#peak_bin = hist.GetMaximumBin()
# Find maximum y-value
ymax = hist.GetMaximum()
ymax_scaled = ymax * 4
hist.SetMaximum(ymax_scaled)

#peak_value = hist.GetXaxis().GetBinCenter(peak_bin)
#print(f"{label}: peak at area_new[{Ch}] = {peak_value:.3f}")

# ─── Landau fit ───────────────────────────────────────────────
fit = ROOT.TF1(f"landau_fit", "landau", xmin, xmax)
hist.Fit(fit, "RQ")  # "R" for range, "Q" for quiet mode
fit.SetLineColor(ROOT.kRed)
fit.SetLineWidth(2)
fit.Draw("same")
mpv = fit.GetParameter(1)  # Landau: [0]=norm, [1]=MPV, [2]=sigma
# fit quality check (Chi2/NDF has to be ~ 1)
fit_result = hist.Fit(fit, "S") # S: silent + return result
chi2 = fit_result.Chi2()
ndf = fit_result.Ndf()
reduced_chi2 = chi2 / ndf if ndf != 0 else float('inf')
prob = fit_result.Prob()

print(f"Bias Voltage={BV} V, Ch-{Ch}: {Sensor}")
print(f"Landau Fit:------------------")
print(f"Reduced Chi2 (Chi2/NDF) = {reduced_chi2:.2f} (has to be 1)")
print(f"Fit Probability (p-value) = {prob:.4f} (has to >= 0.05)")
print(f"pmax > {pmaxCut}: MPV = {mpv:.3f}, Q_collection = {mpv/4.7:.3f}")

# Redraw with fit
#hist.Draw("same")

legend = ROOT.TLegend(0.32, 0.5, 0.89, 0.88)
legend.SetBorderSize(0)
legend.SetFillStyle(0)
legend.SetTextSize(0.034)
legend.SetHeader(f"#bf{{{Sensor}}} pulse area BV #bf{{{BV}}}, pmax >{pmaxCut} mV\n", "L")
legend.AddEntry(fit, f"Landau fit", "l")
legend.AddEntry(0, f"#chi^{{2}}/ndf {reduced_chi2:.1f}, p-val {prob:.3f}", "")
legend.AddEntry(0, f"MPV {mpv:.2f}", "")
legend.AddEntry(0, f"#bf{{Q}}_{{Collection}}(=MPV/4.7) = #bf{{{mpv/4.7:.3f}}}", "")
legend.Draw()


# ─── Alternative Landau X Gaussian convolution fit ──────────────
if altFit:
    print("\nAlternative Fit: Landau X Gaussian Convolution:----------------")

    conv_fit = ROOT.TF1("landau_fit", landaufun, xmin, xmax, 4)
    conv_fit.SetParNames("Width", "MPV", "Area", "GSigma")
    conv_fit.SetParameters(fit.GetParameter(2), mpv, hist.Integral(), 5)
    conv_fit.SetLineColor(ROOT.kGreen+1)
    conv_fit.SetLineStyle(2)
    hist.Fit(conv_fit, "RQ+")
    conv_result = hist.Fit(conv_fit, "S")
    conv_mpv = conv_fit.GetMaximumX(xmin, xmax)
    conv_chi2 = conv_result.Chi2()
    conv_ndf = conv_result.Ndf()
    conv_reduced_chi2 = conv_chi2 / conv_ndf if conv_ndf != 0 else float('inf')
    conv_prob = conv_result.Prob()

    print(f"  Chi2/NDF = {conv_reduced_chi2:.2f}, p-value = {conv_prob:.4f}")
    print(f"pmax > {pmaxCut}: MPV = {conv_mpv:.3f}, Q_collection = {conv_mpv/4.7:.3f}")

    legend.AddEntry(conv_fit, f"Landau #otimes Gaussian convolution fit ", "l")
    legend.AddEntry(0, f"#chi^{{2}}/ndf {conv_reduced_chi2:.1f}, p-val {conv_prob:.3f}", "")
    legend.AddEntry(0, f"MPV {conv_mpv:.2f}", "")
    legend.AddEntry(0, f"#bf{{Q}}_{{Collection}} = #bf{{{conv_mpv/4.7:.3f}}}", "")
    # Redraw with fit
    conv_fit.Draw("same")

c1.Update()
c1.SaveAs(f"hQC_{Sensor}_bv{BV}_pmax{pmaxCut}.png")
