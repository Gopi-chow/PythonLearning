-rc s80     -ep k7           -cr cfg4                 -dm 3ddr    -lc x4 -p a72     -si es2_cpmrc  -pj everest  -rt 1800 -msg "BURST s80 sil all regr" -bep nwlpcie
-rc s80     -ep k7           -cr cfg4                 -dm 3ddr    -lc x4 -p a72 -be -si es2_cpmrc  -pj everest  -rt 1800 -msg "BURST s80 sil all regr" -bep nwlpcie
-rc s80     -ep k7           -cr cfg4                 -dm 3ddr    -lc x4 -p a72     -si es2_cpmrc  -pj everest  -rt 1800 -msg "BURST s80 sil all regr" -bep plb2pcie
-rc s80     -ep k7           -cr cfg4                 -dm 3ddr    -lc x4 -p a72 -be -si es2_cpmrc  -pj everest  -rt 1800 -msg "BURST s80 sil all regr" -bep plb2pcie
-rc s80     -ep s80v350      -cr cfg4 -cm a0cci       -dm 3ddr    -lc x8 -p a72     -si es2_cpmrc  -pj everest  -rt 1800 -msg "BURST s80 sil all regr"
-rc s80     -ep s80v350      -cr cfg4 -cm a0cci       -dm 3ddr    -lc x8 -p a72 -be -si es2_cpmrc  -pj everest  -rt 1800 -msg "BURST s80 sil all regr"
-rc s80     -ep s80v350      -cr cfg4 -cm a0cci       -dm 3ddr    -lc x8 -p a72     -si es2_cpmrc  -pj everest  -rt 1800 -msg "BURST s80 sil all regr"
-rc s80     -ep s80v350      -cr cfg4 -cm a0cci       -dm 3ddr    -lc x8 -p a72 -be -si es2_cpmrc  -pj everest  -rt 1800 -msg "BURST s80 sil all regr"
#-rc s80     -ep s80v350      -cr cfg4 -cm a1          -dm 3ddr    -lc x8 -p a72     -si es2_cpmrc  -pj everest  -rt 1800 -msg "BURST s80 sil all regr"
#-rc s80     -ep s80v350      -cr cfg4 -cm a1          -dm 3ddr    -lc x8 -p a72 -be -si es2_cpmrc  -pj everest  -rt 1800 -msg "BURST s80 sil all regr"
-rc x86     -ep s80v350               -cm qdma        -dm qddr    -lc x8 -p x86     -si es2_cpmep  -pj everest  -rt 1800 -msg "BURST s80 sil all regr" 
