#-b protium        -si h10_cpm5_es1_6_0 -bup                          -p a72     -bt "SPP_PS_ME_CPM,reserved-burst-H10" 
#-b protium        -si h10_cpm5_es1_6_0 -bup                          -p a72 -be -bt "SPP_PS_ME_CPM,reserved-burst-H10" 
#-b protium        -si h10_cpm5_es1_6_0 -bup                          -p r5      -bt "SPP_PS_ME_CPM,reserved-burst-H10" 
#-rc cpm5 -ep cpm5 -si h10_cpm5_es1_6_0 -pj everest -cm plst   -lc x4 -p a72 -bt "SPP_PS_ME_CPM,reserved-burst-H10"
#-rc cpm5 -ep cpm5 -si h10_cpm5_es1_6_0 -pj everest -cm qdma   -lc x4 -p a72 -bt "SPP_PS_ME_CPM,reserved-burst-H10"
#-rc cpm5 -ep cpm5 -si h10_cpm5_es1_6_0 -pj everest -cm epchi1       -lc x4 -p a72 -k Ccix_pcie_sbsx_hnf_id=0x8, -bt "SPP_PS_ME_CPM,reserved-burst-H10"
#-rc cpm5 -ep cpm5 -si h10_cpm5_es1_6_0 -pj everest -cm epchi1       -lc x4 -p a72 -k Ccix_pcie_sbsx_hnf_id=0x0, -bt "SPP_PS_ME_CPM,reserved-burst-H10"
#-rc cpm5 -ep cpm5 -si h10_cpm5_es1_6_0 -pj everest -cm epchi1       -lc x4 -p a72 -k Ccix_pcie_sbsx_hnf_id=0x4, -bt "SPP_PS_ME_CPM,reserved-burst-H10"
#-rc cpm5 -ep cpm5 -si h10_cpm5_es1_6_0 -pj everest -cm epchi1       -lc x4 -p a72 -k Ccix_pcie_sbsx_hnf_id=0xc, -bt "SPP_PS_ME_CPM,reserved-burst-H10"
#-rc cpm5 -ep cpm5 -si h10_cpm5_es1_6_0 -pj everest -cm epchi1opttlp -lc x4 -p a72 -bt "SPP_PS_ME_CPM,reserved-burst-H10"
#-rc cpm5 -ep cpm5 -si h10_cpm5_es1_6_0 -pj everest -cm epcxs        -lc x4 -p a72 -k Ccix_pcie_sbsx_hnf_id=0x8, -bt "SPP_PS_ME_CPM,reserved-burst-H10"
#-rc cpm5 -ep cpm5 -si h10_cpm5_es1_6_0 -pj everest -cm epcxs        -lc x4 -p a72 -k Ccix_pcie_sbsx_hnf_id=0x0, -bt "SPP_PS_ME_CPM,reserved-burst-H10"
#-rc cpm5 -ep cpm5 -si h10_cpm5_es1_6_0 -pj everest -cm epcxs        -lc x4 -p a72 -k Ccix_pcie_sbsx_hnf_id=0x4, -bt "SPP_PS_ME_CPM,reserved-burst-H10"
#-rc cpm5 -ep cpm5 -si h10_cpm5_es1_6_0 -pj everest -cm psccix       -lc x4 -p a72 -k Ccix_pcie_sbsx_hnf_id=0x8, -bt "SPP_PS_ME_CPM,reserved-burst-H10"
#-rc cpm5 -ep cpm5 -si h10_cpm5_es1_6_0 -pj everest -cm psccix       -lc x4 -p a72 -k Ccix_pcie_sbsx_hnf_id=0x4, -bt "SPP_PS_ME_CPM,reserved-burst-H10"
#-rc cpm5 -ep cpm5 -si h10_cpm5_es1_6_0 -pj everest -cm psccix       -lc x4 -p a72 -k Ccix_pcie_sbsx_hnf_id=0x0, -bt "SPP_PS_ME_CPM,reserved-burst-H10"
#-rc cpm5 -ep cpm5 -si h10_cpm5_es1_6_0 -pj everest -cm psccix       -lc x4 -p a72 -k Ccix_pcie_sbsx_hnf_id=0xc, -bt "SPP_PS_ME_CPM,reserved-burst-H10"
#-rc cpm5 -ep cpm5 -si h10_cpm5_es1_6_0 -pj everest -cm rccxs        -lc x4 -p a72 -bt "SPP_PS_ME_CPM,reserved-burst-H10"
