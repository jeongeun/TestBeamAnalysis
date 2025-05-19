import ROOT
from array import array

filename = "Final_SPS-MAY-2025_Data.txt"
# 1column Sensor, 2column BV, 3column timing resolution, 4column chqrge collection

# dictionary for each pmax_fit cut
data = {
        "K2_1"   : [], 
        "K2_2"   : [],
        "K1_50"  : [], 
        "K1_100" : [], 
        }

# read txt
with open(filename) as f:
    for line in f:
        if line.strip().startswith("#") or not line.strip():
            continue
        tokens = line.strip().split()
        if len(tokens) != 4:
            continue
        sensor, bv, tr, qc = tokens[0], int(tokens[1]), float(tokens[2]), float(tokens[3])
        if sensor in data:
            data[sensor].append((bv, tr, qc ))

colors = {
        "K1_100": ROOT.kRed, 
        "K1_50" : ROOT.kOrange+2, 
        "K2_1"  : ROOT.kBlue, 
        "K2_2"  : ROOT.kGreen+2
        }

#define make_graph function
def make_graphs(x_index, y_index, title, x_label, y_label, output, legend_position=(0.15, 0.6, 0.65, 0.88)):
    canvas = ROOT.TCanvas(output, title, 800, 600)
    canvas.SetGrid()
    legend = ROOT.TLegend(*legend_position)
    graphs = []
    first = True

    for sensor, points in data.items():
        points_sorted = sorted(points, key=lambda p: p[0])  # sort by BV
        x = [p[x_index] for p in points_sorted]
        y = [p[y_index] for p in points_sorted]
        # draw graph
        graph = ROOT.TGraph(len(x), array("d", x), array("d", y))
        graph.SetLineColor(colors[sensor])
        graph.SetLineWidth(2)
        graph.SetMarkerStyle(33)#(20)
        graph.SetMarkerSize(3)
        graph.SetMarkerColor(colors[sensor])
        drawopt = "ALP" if first else "LP same"
        graph.Draw(drawopt)
        if first:
            graph.SetTitle(f"{title};{x_label};{y_label}")
            graph.GetXaxis().SetTitleSize(0.05)
            graph.GetXaxis().SetTitleOffset(0.9)
            graph.GetYaxis().SetTitleSize(0.05)
            graph.GetYaxis().SetTitleOffset(0.9)
            first = False
        legend.AddEntry(graph, f"LGAD {sensor}", "lp")
        legend.SetTextSize(0.04)
        graphs.append(graph)

    legend.SetBorderSize(0)
    legend.SetFillStyle(0)
    legend.Draw()
    canvas.Update()
    canvas.SaveAs(output)

# canvas 1 Qc vs. BV
make_graphs(
    x_index=0, y_index=2,
    title="Charge Collection vs Bias Voltage",
    x_label="Bias Voltage (V)",
    y_label="Q_{collection} (fC)",
    output="gr_Qcollection_vs_BV.png",
    legend_position=(0.15, 0.6, 0.65, 0.88)
)

# canvas 2 TR vs. BV
make_graphs(
    x_index=0, y_index=1,
    title="Time Resolution vs Bias Voltage",
    x_label="Bias Voltage (V)",
    y_label="Time Resolution (ps)",
    output="gr_TR_vs_BV.png",
    legend_position=(0.15, 0.15, 0.65, 0.45)
    )

# canvas 3
make_graphs(
    x_index=2, y_index=1,
    title="Time Resolution vs Charge Collection",
    x_label="Q_{collection} (fC)",
    y_label="Time Resolution (ps)",
    output="gr_TR_vs_Qcollection.png",
    legend_position=(0.45, 0.6, 0.88, 0.88)

)
