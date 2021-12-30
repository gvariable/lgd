import ipdb

bws, rtrys, cwnds, rtts, netpwrs = [], [], [], [], []
with open(f"./awesome-env.log") as f:
    for line in f.readlines():
        if "bits/sec" in line:
            line = line.replace("-", ' ')
            line = line.replace("/", ' ')
            fields = line.strip().split()
            bws.append(float(fields[7]))
            rtrys.append(float(fields[12]))
            cwnds.append(int(fields[13][:-1])) # k
            rtts.append(int(fields[14]))
            netpwrs.append(float(fields[-1]))

# 7(BW) 10(Write) 11(err) 12(Rtry) 13(cwnd) 14(Rtt) -1(NetPwr)

print(bws, rtrys, cwnds, rtts, netpwrs)
