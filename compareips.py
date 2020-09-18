with open('cisco.txt','r') as f:
    output_a = [i for i in f]
with open('nexpose.txt','r') as f:
    output_b = [i for i in f]


incisconotinnexpose = set(output_a) - set(output_b)

for delta in incisconotinnexpose:
	print delta.strip('\n')
