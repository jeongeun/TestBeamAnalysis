import ROOT
from array import array

filename = "qcollection_data.txt"
# dictionary for each pmax_fit cut
data = {
        10: [], 
        15: [], 
        18: [], 
        20: []
        }

# read txt
with open(filename) as f:
    for line in f:
        if line.strip().startswith("#") or not line.strip():
            continue
        tokens = line.strip().split()
        if len(tokens) != 3:
            continue
        pmax, bv, q = int(tokens[0]), float(tokens[1]), float(tokens[2])
        if pmax in data:
            data[pmax].append((bv, q))

colors = {
        10: ROOT.kBlue, 
        15: ROOT.kMagenta, 
        18: ROOT.kOrange+2, 
        20: ROOT.kGreen+2
        }

# 1st Canvas & Legend
c1 = ROOT.TCanvas("c", "Qcollection vs Bias Voltage", 800, 600)
c1.SetGrid()
legend = ROOT.TLegend(0.15, 0.6, 0.68, 0.88)

graphs = []
first = True
for pmax, points in data.items():
    x, y = zip(*sorted(points))  # Sorted by Bias V
    graph = ROOT.TGraph(len(x), array("d", x), array("d", y))
    graph.SetLineColor(colors[pmax])
    graph.SetLineWidth(2)
    graph.SetMarkerStyle(20)
    graph.SetMarkerColor(colors[pmax])
    drawopt = "ALP" if first else "LP same"
    graph.Draw(drawopt)
    legend.AddEntry(graph, f"Noise cut (pmax_fit > {pmax} mV)", "lp")
    graphs.append(graph)
    if first:
        graph.SetTitle("Charge Collection of K1 (half-irrad);Bias Voltage (V);Q_{collection} (fC)")
        graph.GetXaxis().SetTitleSize(0.05)
        graph.GetXaxis().SetTitleOffset(0.9)
        graph.GetYaxis().SetTitleSize(0.05)
        graph.GetYaxis().SetTitleOffset(0.9)
        first = False

legend.SetBorderSize(0)
legend.SetFillStyle(0)
legend.Draw()
c1.Update()
c1.SaveAs("gr_K1-half-irrad_Qcollection_vs_bv.png")



### 2nd canvas with Qcollection mean and error bar

c2 = ROOT.TCanvas("c2", "Mean Qcollection with Error Band", 800, 600)
c2.SetGrid()

from collections import defaultdict

# Group all Qcollection values by bias voltage
bv_grouped = defaultdict(list)
for cut_val, points in data.items():
    for bv, q in points:
        bv_grouped[bv].append(q)

# Sort the bias voltages
bv_sorted = sorted(bv_grouped.keys())

# Arrays for mean and symmetric error
x_mean = array("d", [])
y_mean = array("d", [])
ex_mean = array("d", [])
ey_mean = array("d", [])

# Calculate the mean Qcollection and error range for each bias voltage
for bv in bv_sorted:
    q_vals = bv_grouped[bv]
    if len(q_vals) < 2:
        continue
    mean = sum(q_vals) / len(q_vals)
    err_low = mean - min(q_vals)
    err_high = max(q_vals) - mean
    x_mean.append(bv)
    y_mean.append(mean)
    ex_mean.append(0)
    ey_mean.append(max(err_low, err_high)) # symmetric error

y_upper = [y + e for y, e in zip(y_mean, ey_mean)]
y_lower = [y - e for y, e in zip(y_mean, ey_mean)]

x_band = array("d", list(x_mean) + list(reversed(x_mean)))
y_band = array("d", y_upper + list(reversed(y_lower)))

# print out mid qc and error
for i in range(len(x_mean)):
    print(f"Data point {i}: x: {x_mean[i]:.2f} (V), y:{y_mean[i]:.2f} +/- {ey_mean[i]:.3f} (fC)")

# error band (blue)
graph_band = ROOT.TGraph(len(x_band), x_band, y_band)
graph_band.SetFillColorAlpha(ROOT.kAzure + 1, 0.3)
graph_band.SetFillStyle(1001)
graph_band.SetLineWidth(0)

# mid data point and dashed line (black)
graph_mid = ROOT.TGraph(len(x_mean), x_mean, y_mean)
graph_mid.SetLineColor(ROOT.kBlack)
graph_mid.SetLineWidth(3)
graph_mid.SetLineStyle(2)
graph_mid.SetMarkerStyle(20)
graph_mid.SetMarkerSize(1.2)
graph_mid.SetMarkerColor(ROOT.kBlack)
graph_mid.SetFillStyle(1001)
graph_mid.SetFillColorAlpha(ROOT.kAzure + 1, 0.3)

graph_band.SetTitle("Mean Charge Collection with Error Band;Bias Voltage (V);Q_{collection} (fC)")
graph_band.GetXaxis().SetTitleSize(0.05)
graph_band.GetXaxis().SetTitleOffset(0.9)
graph_band.GetYaxis().SetTitleSize(0.05)
graph_band.GetYaxis().SetTitleOffset(0.9)

graph_band.GetXaxis().SetRangeUser(400, 600)
graph_band.GetYaxis().SetRangeUser(3, 6.)

graph_band.Draw("AF")      # Filled area first
graph_mid.Draw("LP SAME")  # Line and points over it
legend2 = ROOT.TLegend(0.15, 0.75, 0.78, 0.88)
legend2.AddEntry(graph_mid, "K1 (half-irradiated) w/ error band", "lfp")
legend2.SetBorderSize(0)
legend2.SetFillStyle(0)
legend2.Draw()

c2.Update()
c2.SaveAs("gr_K1-half-irrad_QC_mean_with_filled_band.png")
