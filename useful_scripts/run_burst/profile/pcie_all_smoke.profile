-rc v7  -ep v7 -lc x4 -p mb  -si prod -pj virtex7 -brc axipcie -bep axipcie  -rt 3600
#-rc k7  -ep k7 -lc x4 -p mb  -si prod -pj kintex7 -brc axipcie -bep axipcie -rt 3600
#-rc k7  -ep k7 -lc x4 -p mb  -si prod -pj kintex7 -brc axipcie -bep nwlpcie -rt 3600
#-rc k7  -ep k7 -lc x4 -p mb  -si prod -pj kintex7 -brc nwlpcie -bep axipcie -rt 3600
-rc k7  -ep k7 -lc x4 -p mb  -si prod -pj kintex7 -brc nwlpcie -bep nwlpcie  -rt 3600
-rc k7  -ep k7 -lc x4 -p mb  -si prod -pj kintex7 -brc nwlpcie -bep plb2pcie -rt 3600
-rc x86 -ep k7 -lc x4 -p x86 -si prod -pj kintex7              -bep axipcie  -rt 3600
-rc x86 -ep k7 -lc x4 -p x86 -si prod -pj kintex7              -bep nwlpcie  -rt 3600
-rc alto    -ep alto    -lc x1 -p a53 -si da7_prod    -rt 3600
-rc alto    -ep alto    -lc x1 -p r5  -si da7_prod    -rt 3600
-rc alto    -ep alto    -lc x4 -p a53 -si da7_prod    -rt 3600
-rc alto    -ep alto    -lc x4 -p r5  -si da7_prod    -rt 3600
-rc alto    -ep k7      -lc x1 -p a53 -si da7_prod  -bep plb2pcie  -rt 3600
-rc alto    -ep k7      -lc x1 -p r5  -si da7_prod  -bep plb2pcie  -rt 3600
-rc alto    -ep k7      -lc x4 -p a53 -si da7_prod  -bep plb2pcie  -rt 3600
-rc alto    -ep k7      -lc x4 -p r5  -si da7_prod  -bep plb2pcie  -rt 3600
#-rc k7      -ep alto    -lc x4 -p mb  -si da7_prod  -brc nwlpcie   -rt 3600
