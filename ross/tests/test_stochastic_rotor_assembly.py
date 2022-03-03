"""Tests file.

Tests for:
    st_rotor_assembly.py
"""
import numpy as np
import pytest
from numpy.testing import assert_allclose

from ross.bearing_seal_element import BearingElement
from ross.disk_element import DiskElement
from ross.materials import steel
from ross.shaft_element import ShaftElement
from ross.stochastic.st_bearing_seal_element import ST_BearingElement
from ross.stochastic.st_disk_element import ST_DiskElement
from ross.stochastic.st_point_mass import ST_PointMass
from ross.stochastic.st_rotor_assembly import ST_Rotor, st_rotor_example
from ross.stochastic.st_shaft_element import ST_ShaftElement


@pytest.fixture
def rotor1():
    # rotor with 6 shaft elements, 2 disks and 2 random bearings
    i_d = 0
    o_d = 0.05
    n = 6
    L = [0.25 for _ in range(n)]

    shaft_elem = [ShaftElement(l, i_d, o_d, material=steel) for l in L]

    disk0 = DiskElement.from_geometry(
        n=2, material=steel, width=0.07, i_d=0.05, o_d=0.28
    )
    disk1 = DiskElement.from_geometry(
        n=4, material=steel, width=0.07, i_d=0.05, o_d=0.28
    )

    kxx = [1e6, 2e6]
    cxx = [1e3, 2e3]
    bearing0 = ST_BearingElement(n=0, kxx=kxx, cxx=cxx, is_random=["kxx", "cxx"])
    bearing1 = ST_BearingElement(n=6, kxx=kxx, cxx=cxx, is_random=["kxx", "cxx"])

    return ST_Rotor(shaft_elem, [disk0, disk1], [bearing0, bearing1])


###############################################################################
# testing error messages
###############################################################################
def test_st_shaft_elements_odd_length():
    tim0 = ST_ShaftElement(
        L=[1, 1.1],
        idl=0,
        odl=[0.1, 0.2],
        material=steel,
        is_random=["L", "odl"],
    )
    tim1 = ST_ShaftElement(
        L=[1, 1.1, 1.2],
        idl=0,
        odl=[0.1, 0.2, 0.3],
        material=steel,
        is_random=["L", "odl"],
    )
    shaft_elm = [tim0, tim1]

    with pytest.raises(ValueError) as ex:
        ST_Rotor(shaft_elm)
    assert "not all random shaft elements lists have same length." in str(ex.value)


def test_st_disk_elements_odd_length():
    tim0 = ShaftElement(L=0.25, idl=0, odl=0.05, material=steel)
    tim1 = ShaftElement(L=0.25, idl=0, odl=0.05, material=steel)
    shaft_elm = [tim0, tim1]

    disk0 = ST_DiskElement(n=0, m=[20, 30], Id=1, Ip=1, is_random=["m"])
    disk1 = ST_DiskElement(n=2, m=[20, 30, 40], Id=1, Ip=1, is_random=["m"])

    with pytest.raises(ValueError) as ex:
        ST_Rotor(shaft_elm, [disk0, disk1])
    assert "not all random disk elements lists have same length." in str(ex.value)


def test_st_bearing_elements_odd_length():
    tim0 = ShaftElement(
        L=0.25,
        idl=0,
        odl=0.05,
        material=steel,
    )
    tim1 = ShaftElement(
        L=0.25,
        idl=0,
        odl=0.05,
        material=steel,
    )
    shaft_elm = [tim0, tim1]

    disk0 = DiskElement(n=1, m=20, Id=1, Ip=1)

    brg0 = ST_BearingElement(
        n=0,
        kxx=[1e6, 2e6],
        cxx=[1e3, 2e3],
        is_random=["kxx", "cxx"],
    )
    brg1 = ST_BearingElement(
        n=2,
        kxx=[1e6, 2e6, 3e6],
        cxx=[1e3, 2e3, 3e3],
        is_random=["kxx", "cxx"],
    )

    with pytest.raises(ValueError) as ex:
        ST_Rotor(shaft_elm, [disk0], [brg0, brg1])
    assert "not all random bearing elements lists have same length." in str(ex.value)


def test_st_point_mass_elements_odd_length():
    tim0 = ShaftElement(L=0.25, idl=0, odl=0.05, material=steel)
    tim1 = ShaftElement(L=0.25, idl=0, odl=0.05, material=steel)
    shaft_elm = [tim0, tim1]

    disk0 = DiskElement(n=1, m=20, Id=1, Ip=1)

    brg0 = BearingElement(n=0, kxx=1e6, cxx=1e3, n_link=3)
    brg1 = BearingElement(n=2, kxx=1e6, cxx=1e3, n_link=4)
    sup0 = BearingElement(n=3, kxx=1e6, cxx=1e3)
    sup1 = BearingElement(n=4, kxx=1e6, cxx=1e3)

    pm0 = ST_PointMass(n=3, m=[1, 2], is_random=["m"])
    pm1 = ST_PointMass(n=4, m=[1, 2, 3], is_random=["m"])

    with pytest.raises(ValueError) as ex:
        ST_Rotor(shaft_elm, [disk0], [brg0, brg1, sup0, sup1], [pm0, pm1])
    assert "not all random point mass lists have same length." in str(ex.value)


def test_elements_odd_length():
    tim0 = ST_ShaftElement(
        L=[1, 1.1],
        idl=0,
        odl=[0.1, 0.2],
        material=steel,
        is_random=["L", "odl"],
    )
    shaft_elm = [tim0, tim0]

    disk0 = ST_DiskElement(n=0, m=[20, 30, 40], Id=1, Ip=1, is_random=["m"])
    disk1 = ST_DiskElement(n=2, m=[20, 30, 40], Id=1, Ip=1, is_random=["m"])
    disks = [disk0, disk1]

    brg0 = ST_BearingElement(
        n=0,
        kxx=[1e6, 2e6],
        cxx=[1e3, 2e3],
        is_random=["kxx", "cxx"],
    )
    brg1 = ST_BearingElement(
        n=2,
        kxx=[1e6, 2e6],
        cxx=[1e3, 2e3],
        is_random=["kxx", "cxx"],
    )
    bearings = [brg0, brg1]

    with pytest.raises(ValueError) as ex:
        ST_Rotor(shaft_elm, disks, bearings)
    assert "not all the random elements lists have the same length." in str(ex.value)


def test_getter_and_setter_error_messages():
    rotor = st_rotor_example()
    with pytest.raises(KeyError) as ex:
        rotor["odd"]
    assert "Object does not have parameter: odd." in str(ex.value)

    with pytest.raises(KeyError) as ex:
        rotor["odd"] = 0
    assert "Object does not have parameter: odd." in str(ex.value)


###############################################################################
# testing methods
###############################################################################
def test_run_campbell(rotor1):
    speed_range = np.linspace(0, 300, 11)
    results = rotor1.run_campbell(speed_range)

    # fmt: off
    wd = np.array([
       [[96.37993790, 107.69984343], [96.31442399, 107.59665761],
        [96.24864330, 107.49310785], [96.18259489, 107.38919370],
        [96.11627780, 107.28491475], [96.04969111, 107.18027058],
        [95.98283388, 107.07526081], [95.91570517, 106.96988508],
        [95.84830408, 106.86414304], [95.78062967, 106.75803436],
        [95.71268103, 106.65155874]],

       [[96.37993790, 107.69984343], [96.44518597, 107.80266577],
        [96.51016917, 107.90512511], [96.57488843, 108.00722194],
        [96.63934474, 108.10895678], [96.70353904, 108.21033015],
        [96.76747229, 108.31134261], [96.83114548, 108.41199472],
        [96.89455957, 108.51228706], [96.95771553, 108.61222022],
        [97.02061433, 108.71179481]],

       [[298.26815963, 366.00322751], [297.24844811, 365.08745483],
        [296.22737131, 364.16826537], [295.20500098, 363.24569809],
        [294.18140949, 362.31979308], [293.15666973, 361.39059156],
        [292.13085515, 360.45813589], [291.10403969, 359.52246953],
        [290.07629773, 358.58363707], [289.04770409, 357.64168422],
        [288.01833396, 356.69665776]],

       [[298.26815963, 366.00322751], [299.28643470, 366.91554560],
        [300.30320286, 367.82437242], [301.31839430, 368.72967244],
        [302.33193991, 369.63141127], [303.34377136, 370.52955566],
        [304.35382106, 371.42407350], [305.36202222, 372.31493382],
        [306.36830887, 373.20210678], [307.37261591, 374.08556367],
        [308.37487908, 374.96527690]],

       [[757.74833789, 939.26471534], [753.12163732, 934.22320534],
        [748.46165664, 929.09822301], [743.76968677, 923.88961209],
        [739.04708033, 918.59746959], [734.29525025, 913.22216688],
        [729.51566813, 907.76436890], [724.70986225, 902.22505055],
        [719.87941530, 896.60551007], [715.02596181, 890.90737861],
        [710.15118520, 885.13262571]],

       [[757.74833789, 939.26471534], [762.34053017, 944.22313987],
        [766.89704950, 949.09907285], [771.41679528, 953.89329143],
        [775.89873122, 958.60673220], [780.34188532, 963.24046803],
        [784.74534972, 967.79568581], [789.10828022, 972.27366533],
        [793.42989571, 976.67575975], [797.70947737, 981.00337746],
        [801.94636773, 985.25796579]],
    ])

    log_dec = np.array([
       [[0.12084052, 0.08299255], [0.12050494, 0.08266962],
        [0.12016825, 0.08234609], [0.11983047, 0.08202195],
        [0.11949159, 0.08169722], [0.11915161, 0.08137189],
        [0.11881054, 0.08104598], [0.11846837, 0.08071950],
        [0.11812511, 0.08039246], [0.11778076, 0.08006485],
        [0.11743533, 0.07973669]],

       [[0.12084052, 0.08299255], [0.12117501, 0.08331485],
        [0.12150839, 0.08363653], [0.12184067, 0.08395758],
        [0.12217185, 0.08427799], [0.12250192, 0.08459776],
        [0.12283089, 0.08491687], [0.12315876, 0.08523533],
        [0.12348552, 0.08555312], [0.12381118, 0.08587024],
        [0.12413573, 0.08618669]],

       [[0.61913530, 0.51868663], [0.62004766, 0.51992251],
        [0.62093892, 0.52114782], [0.62180879, 0.52236224],
        [0.62265701, 0.52356544], [0.62348330, 0.52475710],
        [0.62428740, 0.52593690], [0.62506904, 0.52710451],
        [0.62582798, 0.52825961], [0.62656398, 0.52940188],
        [0.62727680, 0.53053101]],

       [[0.61913530, 0.51868663], [0.61820214, 0.51744051],
        [0.61724848, 0.51618446], [0.61627461, 0.51491881],
        [0.61528085, 0.51364388], [0.61426751, 0.51235999],
        [0.61323492, 0.51106746], [0.61218338, 0.50976661],
        [0.61111324, 0.50845774], [0.61002483, 0.50714118],
        [0.60891848, 0.50581723]],

       [[1.31300861, 1.92588996], [1.30512986, 1.90591603],
        [1.29710066, 1.88566575], [1.28892572, 1.86516039],
        [1.28061010, 1.84442254], [1.27215919, 1.82347604],
        [1.26357873, 1.80234582], [1.25487476, 1.78105774],
        [1.24605361, 1.75963845], [1.23712187, 1.73811517],
        [1.22808639, 1.71651555]],

       [[1.31300861, 1.92588996], [1.32073260, 1.94556769],
        [1.32829787, 1.96493091], [1.33570087, 1.98396282],
        [1.34293842, 2.00264824], [1.35000777, 2.02097357],
        [1.35690652, 2.03892682], [1.36363268, 2.05649757],
        [1.37018466, 2.07367695], [1.37656123, 2.09045759],
        [1.38276153, 2.10683357]],
    ])
    # fmt: on

    assert results.wd.shape == (6, 11, 2)
    assert results.log_dec.shape == (6, 11, 2)
    assert_allclose(results.wd, wd, atol=1e-6)
    assert_allclose(results.log_dec, log_dec, atol=1e-6)


def test_run_freq_response(rotor1):
    speed_range = np.linspace(0, 300, 21)
    inp = 13
    out = 13
    results = rotor1.run_freq_response(inp, out, speed_range)

    # fmt: off
    magnitude = np.array(
        [
            [1.58882967e-06, 1.33882967e-06],
            [1.62744382e-06, 1.36477912e-06],
            [1.75568617e-06, 1.44916962e-06],
            [2.02223729e-06, 1.61623355e-06],
            [2.57176206e-06, 1.92894907e-06],
            [3.96617624e-06, 2.57268939e-06],
            [1.17272387e-05, 4.36496955e-06],
            [8.12057606e-06, 2.37144586e-05],
            [2.79043057e-06, 5.37770966e-06],
            [1.58518830e-06, 2.26831507e-06],
            [1.06229427e-06, 1.36916161e-06],
            [7.73997926e-07, 9.47212517e-07],
            [5.93360940e-07, 7.04894551e-07],
            [4.70721895e-07, 5.49092077e-07],
            [3.82718554e-07, 4.41362159e-07],
            [3.16945750e-07, 3.62980216e-07],
            [2.66224004e-07, 3.03754535e-07],
            [2.26121060e-07, 2.57674896e-07],
            [1.93759548e-07, 2.20975147e-07],
            [1.67194696e-07, 1.91180171e-07],
            [1.45067953e-07, 1.66599615e-07],
        ]
    )

    phase = np.array(
        [
            [1.450892840e-15,  6.54838413e-16],
            [-4.86629256e-03, -2.87216612e-03],
            [-1.07029194e-02, -6.20826058e-03],
            [-1.90893779e-02, -1.06942332e-02],
            [-3.38321163e-02, -1.77221761e-02],
            [-6.90203580e-02, -3.11077414e-02],
            [-2.65016710e-01, -6.74184855e-02],
            [-2.91045618e+00, -4.82441643e-01],
            [-3.04316120e+00, -3.01198713e+00],
            [-3.07219608e+00, -3.07452670e+00],
            [-3.08401017e+00, -3.09200706e+00],
            [-3.08969118e+00, -3.09965998e+00],
            [-3.09235689e+00, -3.10349082e+00],
            [-3.09320123e+00, -3.10536620e+00],
            [-3.09275565e+00, -3.10604441e+00],
            [-3.09126700e+00, -3.10588094e+00],
            [-3.08883657e+00, -3.10505379e+00],
            [-3.08547772e+00, -3.10365040e+00],
            [-3.08114028e+00, -3.10170577e+00],
            [-3.07571909e+00, -3.09922036e+00],
            [-3.06905308e+00, -3.09616849e+00],
        ]
    )
    # fmt: on

    assert results.freq_resp.shape == (21, 2)
    assert results.velc_resp.shape == (21, 2)
    assert results.accl_resp.shape == (21, 2)
    assert_allclose(np.abs(results.freq_resp), magnitude, atol=1e-6)
    assert_allclose(np.angle(results.freq_resp), phase, atol=1e-6)


def test_run_unbalance_response(rotor1):
    freq_range = np.linspace(0, 500, 21)
    n = 3
    m = [0.001, 0.002]
    p = [0.0, np.pi]
    results = rotor1.run_unbalance_response(n, m, p, freq_range)

    # fmt: off
    forced_resp = np.array(
        [
            [ 0.00000000e+00+0.00000000e+00j,  0.00000000e+00+0.00000000e+00j,
              0.00000000e+00+0.00000000e+00j,  0.00000000e+00+0.00000000e+00j,
              0.00000000e+00+0.00000000e+00j,  0.00000000e+00+0.00000000e+00j,
              0.00000000e+00+0.00000000e+00j,  0.00000000e+00+0.00000000e+00j],
            [ 3.37435976e-07-8.68482070e-09j, -8.68482070e-09-3.37435976e-07j,
              9.00209719e-10+1.45114527e-06j,  1.45114527e-06-9.00209715e-10j,
              6.87245293e-07-8.90049158e-09j, -8.90049158e-09-6.87245293e-07j,
              7.83414977e-10+1.28831088e-06j,  1.28831088e-06-7.83414974e-10j],
            [ 1.75768084e-06-1.01068880e-07j, -1.01068880e-07-1.75768084e-06j,
              4.79346233e-08+7.33456232e-06j,  7.33456232e-06-4.79346233e-08j,
              3.52371378e-06-1.12554546e-07j, -1.12554546e-07-3.52371378e-06j,
              4.17303088e-08+6.48704574e-06j,  6.48704574e-06-4.17303088e-08j],
            [ 7.50676607e-06-9.12209199e-07j, -9.12209199e-07-7.50676607e-06j,
              1.28086454e-06+2.98912386e-05j,  2.98912386e-05-1.28086454e-06j,
              1.46900142e-05-1.21918813e-06j, -1.21918813e-06-1.46900142e-05j,
              1.11573867e-06+2.62670396e-05j,  2.62670396e-05-1.11573867e-06j],
            [-6.18015733e-05-3.00382924e-05j, -3.00382924e-05+6.18015733e-05j,
              1.34528953e-04-2.14597175e-04j, -2.14597175e-04-1.34528953e-04j,
             -1.13214987e-04-6.22904820e-05j, -6.22904820e-05+1.13214987e-04j,
              1.17283028e-04-1.86678717e-04j, -1.86678717e-04-1.17283028e-04j],
            [-1.38700091e-05+2.08259695e-08j,  2.08259695e-08+1.38700091e-05j,
              6.46783937e-06-4.63275792e-05j, -4.63275792e-05-6.46783937e-06j,
             -2.49272456e-05-1.53041944e-06j, -1.53041944e-06+2.49272456e-05j,
              5.64471769e-06-3.97928561e-05j, -3.97928561e-05-5.64471769e-06j],
            [-1.02696016e-05+5.04852144e-07j,  5.04852144e-07+1.02696016e-05j,
              3.99127894e-06-3.09402605e-05j, -3.09402605e-05-3.99127894e-06j,
             -1.76161220e-05-4.52895726e-07j, -4.52895726e-07+1.76161220e-05j,
              3.48788819e-06-2.61160471e-05j, -2.61160471e-05-3.48788819e-06j],
            [-9.35892715e-06+7.25075254e-07j,  7.25075254e-07+9.35892715e-06j,
              3.60633532e-06-2.49610892e-05j, -2.49610892e-05-3.60633532e-06j,
             -1.52457821e-05-1.40815948e-07j, -1.40815948e-07+1.52457821e-05j,
              3.15637404e-06-2.05887194e-05j, -2.05887194e-05-3.15637404e-06j]
        ]
    )

    magnitude = np.array(
        [
            [0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
             0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00],
            [3.37547721e-07, 3.37547721e-07, 1.45114555e-06, 1.45114555e-06,
             6.87302926e-07, 6.87302926e-07, 1.28831112e-06, 1.28831112e-06],
            [1.76058423e-06, 1.76058423e-06, 7.33471896e-06, 7.33471896e-06,
             3.52551093e-06, 3.52551093e-06, 6.48717996e-06, 6.48717996e-06],
            [7.56198800e-06, 7.56198800e-06, 2.99186691e-05, 2.99186691e-05,
             1.47405202e-05, 1.47405202e-05, 2.62907254e-05, 2.62907254e-05],
            [6.87148708e-05, 6.87148708e-05, 2.53278476e-04, 2.53278476e-04,
             1.29219725e-04, 1.29219725e-04, 2.20463721e-04, 2.20463721e-04],
            [1.38700247e-05, 1.38700247e-05, 4.67768911e-05, 4.67768911e-05,
             2.49741818e-05, 2.49741818e-05, 4.01912209e-05, 4.01912209e-05],
            [1.02820033e-05, 1.02820033e-05, 3.11966349e-05, 3.11966349e-05,
             1.76219428e-05, 1.76219428e-05, 2.63479275e-05, 2.63479275e-05],
            [9.38697244e-06, 9.38697244e-06, 2.52202623e-05, 2.52202623e-05,
             1.52464324e-05, 1.52464324e-05, 2.08292598e-05, 2.08292598e-05]
        ]
    )

    phase = np.array(
        [
            [ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
              0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00],
            [-2.57320037e-02, -1.59652833e+00,  1.57017598e+00, -6.20344232e-04,
             -1.29502437e-02, -1.58374657e+00,  1.57018823e+00, -6.08094592e-04],
            [-5.74380212e-02, -1.62823435e+00,  1.56426098e+00, -6.53535122e-03,
             -3.19311660e-02, -1.60272749e+00,  1.56436355e+00, -6.43277924e-03],
            [-1.20925370e-01, -1.69172170e+00,  1.52797169e+00, -4.28246367e-02,
             -8.28045733e-02, -1.65360090e+00,  1.52834509e+00, -4.24512383e-02],
            [-2.68917194e+00,  2.02321704e+00, -1.01083863e+00, -2.58163496e+00,
             -2.63859864e+00,  2.07379034e+00, -1.00985519e+00, -2.58065151e+00],
            [ 3.14009114e+00,  1.56929482e+00, -1.43208193e+00, -3.00287826e+00,
             -3.08027417e+00,  1.63211481e+00, -1.42988392e+00, -3.00068025e+00],
            [ 3.09247234e+00,  1.52167601e+00, -1.44250530e+00, -3.01330162e+00,
             -3.11588915e+00,  1.59649983e+00, -1.43802853e+00, -3.00882486e+00],
            [ 3.06427292e+00,  1.49347659e+00, -1.42731092e+00, -2.99810724e+00,
             -3.13235653e+00,  1.58003245e+00, -1.41867471e+00, -2.98947104e+00]
        ]
    )
    # fmt: on

    assert results.forced_resp.shape == (2, 28, 21)
    assert results.velc_resp.shape == (2, 28, 21)
    assert results.accl_resp.shape == (2, 28, 21)
    assert_allclose(results.forced_resp[0, :8, :8].T, forced_resp, atol=1e-8)
    assert_allclose(np.abs(results.forced_resp[0, :8, :8]).T, magnitude, atol=1e-8)
    assert_allclose(np.angle(results.forced_resp[0, :8, :8]).T, phase, atol=1e-8)


def test_time_response(rotor1):
    size = 5
    ndof = rotor1.ndof
    RV_size = rotor1.RV_size
    node = 3
    speed = 250.0
    t = np.linspace(0, 10, size)
    F = np.zeros((RV_size, size, ndof))

    force = [10, 20]
    for i, f in enumerate(force):
        F[i, :, 4 * node] = f * np.cos(2 * t)
        F[i, :, 4 * node + 1] = f * np.sin(2 * t)
    results = rotor1.run_time_response(speed, F, t)

    # fmt: off
    yout = np.array([
        [
            [ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
              0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00],
            [ 1.41926788e-06, -4.76460045e-06,  2.07102404e-05,  6.16414329e-06,
              2.90572612e-06, -9.75899792e-06,  1.84111116e-05,  5.47908613e-06],
            [-4.19299249e-06, -2.72072007e-06,  1.18190692e-05, -1.82276630e-05,
             -8.58856216e-06, -5.57088030e-06,  1.05060401e-05, -1.62024453e-05],
            [-3.79851214e-06,  3.24877791e-06, -1.41256904e-05, -1.65046953e-05,
             -7.77860208e-06,  6.65516143e-06, -1.25561980e-05, -1.46710490e-05],
            [ 2.03783269e-06,  4.56404302e-06, -1.98336856e-05,  8.86369112e-06,
              4.17529112e-06,  9.34691210e-06, -1.76301510e-05,  7.87880520e-06]
        ],

        [
            [ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
              0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00],
            [ 1.48084281e-06, -4.85047585e-06,  4.21928512e-05,  1.28581579e-05,
              4.58105873e-06, -1.50244567e-05,  3.74957287e-05,  1.14234040e-05],
            [-4.19558895e-06, -2.72284012e-06,  2.36499572e-05, -3.64745372e-05,
             -1.29913427e-05, -8.42599304e-06,  2.10223709e-05, -3.24217457e-05],
            [-3.79910377e-06,  3.24942961e-06, -2.82561248e-05, -3.30133748e-05,
             -1.17602388e-05,  1.00633351e-05, -2.51165462e-05, -2.93455705e-05],
            [ 2.03823954e-06,  4.56492726e-06, -3.96735422e-05,  1.77304732e-05,
              6.31389854e-06,  1.41321453e-05, -3.52656873e-05,  1.57603189e-05]
        ],
    ])
    # fmt: on

    assert results.yout.shape == (2, 5, 28)
    assert_allclose(results.yout[:, :, :8], yout, atol=1e-8)
