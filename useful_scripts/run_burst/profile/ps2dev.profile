-b zcu102 -br rev1.0 -p a53         -dp -clk av     -si da7_prod                                   -rt 1200  -msg "BURST ps dev regr"
-b zcu102 -br rev1.0 -p r5        -dp -clk av     -si da7_prod                                   -rt 1200  -msg "BURST ps dev regr"
-b zcu102 -br rev1.0 -p a53 -be       -clk sivdef -si da7_prod                                   -rt 1200  -msg "BURST ps dev regr"
#-b zc702 -p a9 -si prod                                                                            -rt 1200  -msg "BURST ps dev regr"
#-b zc706 -p a9 -si prod                                                                            -rt 1200  -msg "BURST ps dev regr"
-b tenzing -dc se1 -si es2_pscon4  -dm 3ddr -bupcoh -p a72     -ospi -ecc                          -rt 3600  -msg "BURST ps dev regr"
-b tenzing -dc se1 -si es2_pscon4  -dm 3ddr -bupcoh -p a72 -be -ospi -ecc                          -rt 1800  -msg "BURST ps dev regr"
-b tenzing -dc se1 -si es2_pscon4  -dm 3ddr -bupcoh -p r5      -ospi -ecc                          -rt 1800  -msg "BURST ps dev regr"
-b tenzing -dc se1 -si es2_pscon4  -dm 3ddr -bup    -p a72                                         -rt 3600  -msg "BURST ps dev regr"
-b tenzing -dc se1 -si es2_pscon4  -dm 3ddr -bup    -p a72 -be                                     -rt 1800  -msg "BURST ps dev regr"
-b tenzing -dc se1 -si es2_pscon4  -dm 3ddr -bup    -p r5                                          -rt 1800  -msg "BURST ps dev regr"
-b tenzing -dc se2 -si es2_pscon4  -dm sddr -bup    -p a72                                         -rt 3600  -msg "BURST ps dev regr"
-b tenzing -dc se2 -si es2_pscon4  -dm sddr -bup    -p a72 -be                                     -rt 1800  -msg "BURST ps dev regr"
-b tenzing -dc se2 -si es2_pscon4  -dm sddr -bup    -p r5                                          -rt 1800  -msg "BURST ps dev regr"
-b tenzing -dc se1 -si es2_me      -dm dddr -bup    -p a72                                         -rt 3600  -msg "BURST ps dev regr"
-b tenzing -dc se1 -si es2_me      -dm dddr -bup    -p r5                                          -rt 1800  -msg "BURST ps dev regr"
-b tenzing -dc se1 -si es2_me      -dm dddr -bup    -p a72 -be -k "Me_cardano_enable=1,"           -rt 1800  -msg "BURST ps dev regr"
-b tenzing -dc se1 -si es2_me      -dm dddr -bup    -p r5      -k "Me_cardano_enable=1,"           -rt 1800  -msg "BURST ps dev regr"
-b tenzing -dc se1 -si es2_me      -dm dddr -bup    -p a72     -k "Me_core_enable=0,"              -rt 1800  -msg "BURST ps dev regr"
-b vck190 -si es2_pscon4  -dm sddr -bup -p a72     -rt 1800 -msg "BURST ps dev regr"
-b vck190 -si es2_pscon4  -dm sddr -bup -p a72 -be -rt 1800 -msg "BURST ps dev regr"
-b vck190 -si es2_pscon4  -dm sddr -bup -p r5      -rt 1800 -msg "BURST ps dev regr"
-b tenpro -bt reserved-burst -si aie2_vdu_ipp_5_0 -p a72                                            -rt 3600  -msg "BURST ps dev regr"
-b tenpro -bt reserved-burst -si aie2_vdu_ipp_5_0 -p a72 -be                                        -rt 3600  -msg "BURST ps dev regr"
-rc x86     -ep s80v350           -cm qdma        -dm qddr    -lc x8 -p x86     -si es2_cpmep  -pj everest  -rt 1800 -msg "BURST ps dev regr"
-rc s80     -ep s80v350  -cr cfg4 -cm a0cci       -dm 3ddr    -lc x8 -p a72     -si es2_cpmrc  -pj everest  -rt 1800 -msg "BURST ps dev regr"
-rc s80     -ep s80v350  -cr cfg4 -cm a0cci       -dm 3ddr    -lc x8 -p a72     -si es2_cpmrc  -pj everest  -rt 1800 -msg "BURST ps dev regr" 
#-rc s80     -ep s80v350  -cr cfg4 -cm a1          -dm 3ddr    -lc x8 -p a72     -si es2_cpmrc  -pj everest  -rt 1800 -msg "BURST ps dev regr" 
-rc s80     -ep k7       -cr cfg4                 -dm 3ddr    -lc x4 -p a72     -si es2_cpmrc  -pj everest  -rt 1800 -msg "BURST ps dev regr" -bep plb2pcie
-rc s80     -ep k7       -cr cfg4                 -dm 3ddr    -lc x4 -p a72     -si es2_cpmrc  -pj everest  -rt 1800 -msg "BURST ps dev regr" -bep nwlpcie
-rc s80     -ep k7       -cr cfg4    -be          -dm 3ddr    -lc x4 -p a72     -si es2_cpmrc  -pj everest  -rt 1800 -msg "BURST ps dev regr" -bep nwlpcie
-b xa2785  -si h10_es1_ps  -pj everest   -p a72 -bup      -rt 1800  -msg "BURST ps dev regr"
-b xa2785  -si h10_es1_ps  -pj everest   -p a72 -bup -be  -rt 1800  -msg "BURST ps dev regr"
-b xa2785  -si h10_es1_ps  -pj everest   -p r5  -bup      -rt 1800  -msg "BURST ps dev regr"
-b haps-7  -s 0 -pj ksb -si psxl_spp_v5_0_ddr5 -p a78 -bup     -rt 17400 -msg "BURST ps dev regr"
-b haps-9  -s 1 -pj ksb -si psxl_spp_v5_0_ddr5 -p r52 -bup     -rt  7200 -msg "BURST ps dev regr"
-b haps-12 -s 0 -pj ksb -si psxl_spp_v5_0_ddr5 -p r52-lockstep -bup     -rt 17400 -msg "BURST ps dev regr"
-rc h10 -ep k7      -si h10_es2_cpmrc -pj everest -dm 3ddr    -lc x4  -pg g2 -p a72 -bep plb2pcie -rt 1800 -msg "BURST ps dev regr"
-rc h10 -ep k7      -si h10_es2_cpmrc -pj everest -dm 3ddr    -lc x4  -pg g2 -p a72 -bep nwlpcie  -rt 1800 -msg "BURST ps dev regr"
-rc h10 -ep h10     -si h10_es2_cpmrc -pj everest -cm aximmc1 -lc x8  -pg g5 -p a72 -rt 1800 -msg "BURST ps dev regr"
-rc h10 -ep h10     -si h10_es2_cpmrc -pj everest -cm aximmc0 -lc x8  -pg g5 -p a72 -rt 1800 -msg "BURST ps dev regr"
-rc h10 -ep h10     -si h10_es2_cpmrc -pj everest -cm aximmc0 -lc x16 -pg g4 -p a72 -rt 1800 -msg "BURST ps dev regr"
-rc x86 -ep h10     -si h10_es2_cpmep -pj everest -cm aximm1  -lc x8  -pg g5 -p x86 -rt 1800 -msg "BURST ps dev regr"
-b haps-4 -s 0   -si cpm5n_ipp_v5_0 -pj ksb -rc cpm5n -ep cpm5n --cpm_mode c1c0 --lane_count x4 --processor a72 -rt 7200
-b ph1760       -si jamling_es1       -p a72      -bup     -rt 3600    -msg "BURST ps dev regr"
-b ph1760       -si jamling_es1       -p a72  -be -bup     -rt 3600    -msg "BURST ps dev regr"
-b ph1760       -si jamling_es1       -p r5       -bup     -rt 7200    -msg "BURST ps dev regr"
