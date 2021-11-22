# cconfparse-exp
ciscoconfparse experiment

## Exec

```text
hagiwara@dev02:~/ool-mddo/cconfparse-exp$ python make_intf_prop_table.py -f  ../netomox-exp/model_defs/batfish-test-topology/l2l3/sample3err2/configs/switch1-confg
# parse config = ../netomox-exp/model_defs/batfish-test-topology/l2l3/sample3err2/configs/switch1-confg
# Found config file of switch1
# Table: 
                         Interface Access_VLAN Allowed_VLANs  Channel_Group                           Channel_Group_Members   Primary_Address  Switchport Switchport_mode      VRF
0           switch1[Port-channel1]               100,200-201                 [GigabitEthernet1/0/23, GigabitEthernet1/0/24]                          True           TRUNK  default
1    switch1[GigabitEthernet1/0/1]         100                                                                           []                          True          ACCESS  default
2    switch1[GigabitEthernet1/0/2]         100                                                                           []                          True          ACCESS  default
3    switch1[GigabitEthernet1/0/3]         100                                                                           []                          True          ACCESS  default
4    switch1[GigabitEthernet1/0/4]         100                                                                           []                          True          ACCESS  default
5    switch1[GigabitEthernet1/0/5]         200                                                                           []                          True          ACCESS  default
6    switch1[GigabitEthernet1/0/6]         200                                                                           []                          True          ACCESS  default
7    switch1[GigabitEthernet1/0/7]         200                                                                           []                          True          ACCESS  default
8    switch1[GigabitEthernet1/0/8]         200                                                                           []                          True          ACCESS  default
9    switch1[GigabitEthernet1/0/9]         201                                                                           []                          True          ACCESS  default
10  switch1[GigabitEthernet1/0/10]                                                                                       []                         False            NONE  default
11  switch1[GigabitEthernet1/0/11]                                                                                       []       10.0.1.2/24       False            NONE  default
12  switch1[GigabitEthernet1/0/12]                                                                                       []                         False            NONE  default
13  switch1[GigabitEthernet1/0/13]                                                                                       []                         False            NONE  default
14  switch1[GigabitEthernet1/0/14]                                                                                       []                         False            NONE  default
15  switch1[GigabitEthernet1/0/15]                                                                                       []                         False            NONE  default
16  switch1[GigabitEthernet1/0/16]                                                                                       []                         False            NONE  default
17  switch1[GigabitEthernet1/0/17]                                                                                       []                         False            NONE  default
18  switch1[GigabitEthernet1/0/18]                                                                                       []                         False            NONE  default
19  switch1[GigabitEthernet1/0/19]                                                                                       []                         False            NONE  default
20  switch1[GigabitEthernet1/0/20]                                                                                       []                         False            NONE  default
21  switch1[GigabitEthernet1/0/21]                                                                                       []                         False            NONE  default
22  switch1[GigabitEthernet1/0/22]                                                                                       []                         False            NONE  default
23  switch1[GigabitEthernet1/0/23]                   100,200  Port-channel1                                              []                          True           TRUNK  default
24  switch1[GigabitEthernet1/0/24]                   100,200  Port-channel1                                              []                          True           TRUNK  default
25                  switch1[Vlan1]                                                                                       []                         False            NONE  default
26                switch1[Vlan100]                                                                                       []    192.168.1.2/24       False            NONE  default
27                switch1[Vlan200]                                                                                       []  192.168.2.102/24       False            NONE  testvrf
```
