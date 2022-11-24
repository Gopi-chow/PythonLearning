#Enter tool version for testing in -tv parameter
-b tenpro   -bt reserved-burst                      -si aie2_vdu_ipp_3_0 -p a72          -msg "Tool version update regr" -tv "2021.2_weekly_latest"
-b tenzing  -dc se1 -dm dddr                        -si es2_pscon4       -p a72 -bup -be -msg "Tool version update regr" -tv "2021.2_weekly_latest"
-b xa2785   -pj everest                             -si h10_es1_ps       -p a72 -bup     -msg "Tool version update regr" -tv "2021.2_weekly_latest"
-b zcu102   -br rev1.0 -dp                          -si da7_prod         -p a53 -clk av  -msg "Tool version update regr" -tv "2021.2_weekly_latest"
#-b protium  -bt "SPP_PS_ME_CPM,reserved-burst-H10"  -si h10_cpm5_es2_1_0 -p a72 -bup     -msg "Tool version update regr" -tv "2021.2_weekly_latest"
