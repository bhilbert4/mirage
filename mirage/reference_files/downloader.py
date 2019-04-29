#! /usr/bin /env python

"""Download the reference files needed to run Mirage. Extract and unzip
files, and place into the proper directory. Inform the user how to set
the MIRAGE_DATA encironment variable.
"""
import os
import requests
import shutil
import tarfile
import zipfile

from mirage.utils.utils import ensure_dir_exists


NIRCAM_REFFILES_URL = [('https://stsci.box.com/s/6eomezd68n3surgqut8if6gy8l6lf3xk', 'nircam_reference_files.tar.gz')]
NIRISS_REFFILES_URL = [('https://stsci.box.com/s/evlv7vxszgmiff3zdmdxnol6u6h8pa9j', 'niriss_reference_files.tar.gz')]
FGS_REFFILES_URL = [('https://stsci.box.com/s/ia5z21m69tb08hd5zpv01c43g0px3gfm', 'fgs_reference_files.tar.gz')]

NIRCAM_CR_LIBRARY_URL = [('https://stsci.box.com/s/4cw7wmsqw9qhdozl4owz0tmr6ozusfqr', 'mirage_nircam_cr_library.tar.gz')]
NIRISS_CR_LIBRARY_URL = [('https://stsci.box.com/s/uxyb08cjkf1i7yd4fhryrhi6dr4da9pg', 'mirage_niriss_cr_library.tar.gz')]
FGS_CR_LIBRARY_URL = [('https://stsci.box.com/s/d5oswszqbwt6i027g6ue3usi47dmyign', 'mirage_fgs_cr_library.tar.gz')]



NIRCAM_INDIVIDUAL_PSF_URLS = [('https://stsci.box.com/s/4rw5p9dd8ofa13pnmgfgz1svr8qustcv', 'nircam_a1_subpix_grid_webbpsf_library.tar.gz'),
                              ('https://stsci.box.com/s/ngx0mfo6pppe9zbrvzh28n90fe6v4d6i', 'nircam_a2_subpix_grid_webbpsf_library.tar.gz'),
                              ('https://stsci.box.com/s/nc2tt2w4cbylwy0ny7bxme37xtnd26cm', 'nircam_a3_subpix_grid_webbpsf_library.tar.gz'),
                              ('https://stsci.box.com/s/27bkgppw3ajyhfvl6nnv2wt9mlcn0ae9', 'nircam_a4_subpix_grid_webbpsf_library.tar.gz'),
                              ('https://stsci.box.com/s/gg48crkex2afjqb11replcg0gs2bm5cv', 'nircam_a5_subpix_grid_webbpsf_library.tar.gz'),
                              ('https://stsci.box.com/s/tg2pjk829oc73ijl9kda0j4ccagg75ce', 'nircam_b1_subpix_grid_webbpsf_library.tar.gz'),
                              ('https://stsci.box.com/s/7vmp33fb6hwcyesl39z7v7rcgpq4ls5x', 'nircam_b2_subpix_grid_webbpsf_library.tar.gz'),
                              ('https://stsci.box.com/s/55yf2n72l0xlc6u6t6igv5e8u8zcnunq', 'nircam_b3_subpix_grid_webbpsf_library.tar.gz'),
                              ('https://stsci.box.com/s/5gbse7nhpwnfptpip5bci3uyt0sate4y', 'nircam_b4_subpix_grid_webbpsf_library.tar.gz'),
                              ('https://stsci.box.com/s/b3fepnceqznfmwct9sszoc2lzxl8iaku', 'nircam_b5_subpix_grid_webbpsf_library.tar.gz')]
NIRISS_INDIVIDUAL_PSF_URLS = [('https://stsci.box.com/s/29z7ounfn61gjwi3kiu04hc0f8qgaot9', 'niriss_subpix_grid_f090w_webbpsf_library.tar.gz'),
                              ('https://stsci.box.com/s/i5yhe4zbzxawnah8csdpp4qtk9dmao1t', 'niriss_subpix_grid_f115w_webbpsf_library.tar.gz'),
                              ('https://stsci.box.com/s/s1j1kpx0aes1ntf4qrlyl1mhitj0sz2u', 'niriss_subpix_grid_f140m_webbpsf_library.tar.gz'),
                              ('https://stsci.box.com/s/cc5kjqp78uvtrmlpd0jk6llobajkhavr', 'niriss_subpix_grid_f150w_webbpsf_library.tar.gz'),
                              ('https://stsci.box.com/s/g0lwik43s7erbpsm6r5slq1739bnjob9', 'niriss_subpix_grid_f158m_webbpsf_library.tar.gz'),
                              ('https://stsci.box.com/s/70utbxqfmi474hxb34uawjnrujilj6hb', 'niriss_subpix_grid_f200w_webbpsf_library.tar.gz'),
                              ('https://stsci.box.com/s/jorfqdq56u73wlnj9nk0r34o36ruc8ky', 'niriss_subpix_grid_f277w_webbpsf_library.tar.gz'),
                              ('https://stsci.box.com/s/edafbfzxc4iijr5rzfkziasu64quh6lb', 'niriss_subpix_grid_f356w_webbpsf_library.tar.gz'),
                              ('https://stsci.box.com/s/oqsriubvc0knwtrsoavxj8gi7psz2yck', 'niriss_subpix_grid_f380m_webbpsf_library.tar.gz'),
                              ('https://stsci.box.com/s/i6c28jii139x8dnzxy6bp3fnm25npnvw', 'niriss_subpix_grid_f430m_webbpsf_library.tar.gz'),
                              ('https://stsci.box.com/s/fjep4n3dhw2uavt0uk07dfk65dww1zp8', 'niriss_subpix_grid_f444w_webbpsf_library.tar.gz'),
                              ('https://stsci.box.com/s/3cg3397siwiirv64hpez5uc9oyaey5d8', 'niriss_subpix_grid_f480m_webbpsf_library.tar.gz'),
                              ('https://stsci.box.com/s/rk38t0psx4kmqx5wxqsmlrntzusm4aod', 'niriss_nrm_subpix_grid_f277w_webbpsf_library.tar.gz'),
                              ('https://stsci.box.com/s/x2c99ivjzze0ixdywtoczoyi438mw76m', 'niriss_nrm_subpix_grid_f380m_webbpsf_library.tar.gz'),
                              ('https://stsci.box.com/s/lwwei3atsbo64iz10c3blru5fnbof69u', 'niriss_nrm_subpix_grid_f430m_webbpsf_library.tar.gz'),
                              ('https://stsci.box.com/s/7mxdonrlx9qz1mxmfgjzfg6bqwc5fzi3', 'niriss_nrm_subpix_grid_f480m_webbpsf_library.tar.gz')]

FGS_INDIVIDUAL_PSF_URLS = [('https://stsci.box.com/s/3g8f3i0w24l4yqu0bpin5uei7e5or9uh', 'fgs_subpix_grid_webbpsf_library.tar.gz')]

NIRCAM_GRIDDED_PSF_URLS = []
NIRISS_GRIDDED_PSF_URLS = []
FGS_GRIDDED_PSF_URLS = []

NIRCAM_RAW_DARK_URLS = [('https://stsci.box.com/s/pctjgthruh86ctr6ww9bgzccjlzc0xt3', 'NRCNRCA1-DARK-60082202011_1_481_SE_2016-01-09T00h03m58_level1b_uncal.fits'),
                        ('https://stsci.box.com/s/df2bxy3iwenot0ykti06xqwnn1j9k0ii', 'NRCNRCA1-DARK-60090213141_1_481_SE_2016-01-09T02h53m12_level1b_uncal.fits'),
                        ('https://stsci.box.com/s/rv8x4snxwqznymy92h40c70f7c7k8zh7', 'NRCNRCA1-DARK-60090604481_1_481_SE_2016-01-09T06h52m47_level1b_uncal.fits'),
                        ('https://stsci.box.com/s/v0h1ndnnbgiar4wcx1ynl0ueli4ksz57', 'NRCNRCA1-DARK-60091005411_1_481_SE_2016-01-09T10h56m36_level1b_uncal.fits'),
                        ('https://stsci.box.com/s/c1u5iwte7brjlm2dhqfibbw6ylqyshjv', 'NRCNRCA1-DARK-60091434481_1_481_SE_2016-01-09T15h50m45_level1b_uncal.fits'),
                        ('https://stsci.box.com/s/60mpcp81s7nzmjmb6cbnjvznxqpqbja8', 'NRCNRCA2-DARK-60082224241_1_482_SE_2016-01-09T00h10m36_level1b_uncal.fits'),
                        ('https://stsci.box.com/s/9zbro9it89h6ddipmfjxsakf3mrleb7x', 'NRCNRCA2-DARK-60090235001_1_482_SE_2016-01-09T04h17m03_level1b_uncal.fits'),
                        ('https://stsci.box.com/s/fe96k5h9polxacaewwit01n2ufutndpq', 'NRCNRCA2-DARK-60090635511_1_482_SE_2016-01-09T07h05m19_level1b_uncal.fits'),
                        ('https://stsci.box.com/s/3uw9i5q2uwgsol6q5qb7uzf4c3l295ro', 'NRCNRCA2-DARK-60091030561_1_482_SE_2016-01-09T11h03m17_level1b_uncal.fits'),
                        ('https://stsci.box.com/s/deuxfqva8vd32oblmz3d0wu8683doigs', 'NRCNRCA2-DARK-60091457131_1_482_SE_2016-01-09T15h50m45_level1b_uncal.fits'),
                        ('https://stsci.box.com/s/8mx9ziefvjil6ptsr52bqatg69ssr832', 'NRCNRCA3-DARK-60082245481_1_483_SE_2016-01-09T00h04m26_level1b_uncal.fits'),
                        ('https://stsci.box.com/s/e6pm1zg59k7fdx36x9cxl0kalvd5ewwo', 'NRCNRCA3-DARK-60090321241_1_483_SE_2016-01-09T04h17m10_level1b_uncal.fits'),
                        ('https://stsci.box.com/s/qf90unkzkfb7gv0fhg3n1kkf2hwfc6l8', 'NRCNRCA3-DARK-60090656591_1_483_SE_2016-01-09T07h31m27_level1b_uncal.fits'),
                        ('https://stsci.box.com/s/8p348edl8dh5wr7g2sqnj2tlxae3us9o', 'NRCNRCA3-DARK-60091052561_1_483_SE_2016-01-09T11h28m06_level1b_uncal.fits'),
                        ('https://stsci.box.com/s/zoq314y0jzanpyd0am0cu3f9phoklmzv', 'NRCNRCA3-DARK-60091522581_1_483_SE_2016-01-09T16h30m34_level1b_uncal.fits'),
                        ('https://stsci.box.com/s/sv5npcnyvkfshdsjgi0ooen5edwxsg2e', 'NRCNRCA4-DARK-60082307391_1_484_SE_2016-01-09T00h04m08_level1b_uncal.fits'),
                        ('https://stsci.box.com/s/zgjvynxemydgiu435tpjh7kt30ywk9wp', 'NRCNRCA4-DARK-60090259591_1_484_SE_2016-01-09T04h16m50_level1b_uncal.fits'),
                        ('https://stsci.box.com/s/q8s7f2icgdtnzjd4a2qat9gmm30vqfhj', 'NRCNRCA4-DARK-60090720041_1_484_SE_2016-01-09T07h58m26_level1b_uncal.fits'),
                        ('https://stsci.box.com/s/ya8o0881reg9jncshug5b91mug3trxlk', 'NRCNRCA4-DARK-60091117441_1_484_SE_2016-01-09T11h52m23_level1b_uncal.fits'),
                        ('https://stsci.box.com/s/zifn5ogf7glksnddhptbqbvxioxtw2dm', 'NRCNRCA4-DARK-60091548131_1_484_SE_2016-01-09T16h30m50_level1b_uncal.fits'),
                        ('https://stsci.box.com/s/tjkyvudkgwxsehw6xuizz8bhduy2dkwu', 'NRCNRCALONG-DARK-60082329041_1_485_SE_2016-01-09T00h04m16_level1b_uncal.fits'),
                        ('https://stsci.box.com/s/9kp7zwv88baoqb1v2ajx2x96yubkv1ml', 'NRCNRCALONG-DARK-60090344021_1_485_SE_2016-01-09T04h16m42_level1b_uncal.fits'),
                        ('https://stsci.box.com/s/14osssajxnyfhwnhkmk60ob8u25ymiuq', 'NRCNRCALONG-DARK-60090746381_1_485_SE_2016-01-09T08h21m48_level1b_uncal.fits'),
                        ('https://stsci.box.com/s/f2ntx77wg82padmj4u9wjuzeoxdiy4mq', 'NRCNRCALONG-DARK-60091140151_1_485_SE_2016-01-09T14h23m49_level1b_uncal.fits'),
                        ('https://stsci.box.com/s/ghn59ko04b2msldt089iffc1v3ie7agi', 'NRCNRCALONG-DARK-60091611271_1_485_SE_2016-01-09T17h16m35_level1b_uncal.fits'),
                        ('https://stsci.box.com/s/lfyonc2kuvevakzr10yrgcgjk7rcm6o8', 'NRCNRCB1-DARK-60082356471_1_486_SE_2016-01-09T02h47m00_level1b_uncal.fits'),
                        ('https://stsci.box.com/s/jhhbkxlw47aey5ut93o5xbnk8rrrrcdj', 'NRCNRCB1-DARK-60090405201_1_486_SE_2016-01-09T05h33m56_level1b_uncal.fits'),
                        ('https://stsci.box.com/s/padrxurzkvg4dda9ombf7fto2poqcwtl', 'NRCNRCB1-DARK-60090807581_1_486_SE_2016-01-09T08h48m11_level1b_uncal.fits'),
                        ('https://stsci.box.com/s/bhzkf4uex4yqa2sq0pzt1srhtq6liv13', 'NRCNRCB1-DARK-60091205311_1_486_SE_2016-01-09T14h30m08_level1b_uncal.fits'),
                        ('https://stsci.box.com/s/04m3kxsbtehf7ndvxut70jz814g6lr77', 'NRCNRCB1-DARK-60091636021_1_486_SE_2016-01-09T17h16m13_level1b_uncal.fits'),
                        ('https://stsci.box.com/s/wsifqidhgwixkpjpmqy9i4anhagf361h', 'NRCNRCB2-DARK-60090021181_1_487_SE_2016-01-09T02h51m54_level1b_uncal.fits'),
                        ('https://stsci.box.com/s/dubivztvsafigzm7oghyi7l7hvns3az5', 'NRCNRCB2-DARK-60090427541_1_487_SE_2016-01-09T05h33m14_level1b_uncal.fits'),
                        ('https://stsci.box.com/s/70nmsc1op9mq1uybceh3m5zw547otjgl', 'NRCNRCB2-DARK-60090830131_1_487_SE_2016-01-09T08h59m50_level1b_uncal.fits'),
                        ('https://stsci.box.com/s/qo3b6icrzn3ztd2t27nq1acexb321fqx', 'NRCNRCB2-DARK-60091230011_1_487_SE_2016-01-09T14h23m47_level1b_uncal.fits'),
                        ('https://stsci.box.com/s/jlr9f0uiajyoaf5j3bqas4iqgk7mgxla', 'NRCNRCB2-DARK-60091735131_1_487_SE_2016-01-09T18h09m45_level1b_uncal.fits'),
                        ('https://stsci.box.com/s/b0bfeqkaeqgyblzhl39ufa9t0p8b4vh1', 'NRCNRCB3-DARK-60090043151_1_488_SE_2016-01-09T02h53m21_level1b_uncal.fits'),
                        ('https://stsci.box.com/s/nx7c1ugce6factspliruya3z3t7chkmx', 'NRCNRCB3-DARK-60090451471_1_488_SE_2016-01-09T05h33m25_level1b_uncal.fits'),
                        ('https://stsci.box.com/s/k8uuqkouz5465t5m5238rf327ehly7ol', 'NRCNRCB3-DARK-60090852451_1_488_SE_2016-01-09T09h35m03_level1b_uncal.fits'),
                        ('https://stsci.box.com/s/4wd55isjm8s2zdmqsf5lc9fdiwzopwfh', 'NRCNRCB3-DARK-60091254111_1_488_SE_2016-01-09T14h23m58_level1b_uncal.fits'),
                        ('https://stsci.box.com/s/tr722w87zdvyee35sou62ipjkhgd6z2b', 'NRCNRCB3-DARK-60091757401_1_488_SE_2016-01-09T18h40m55_level1b_uncal.fits'),
                        ('https://stsci.box.com/s/runlc3olxq3b6uw56cf8gq0ck5mx227p', 'NRCNRCB4-DARK-60090118261_1_489_SE_2016-01-09T02h46m53_level1b_uncal.fits'),
                        ('https://stsci.box.com/s/5v9xqtswzuvprgshp2zpunbp5h32izkt', 'NRCNRCB4-DARK-60090513431_1_489_SE_2016-01-09T05h57m50_level1b_uncal.fits'),
                        ('https://stsci.box.com/s/r7hf20hxg2mamfuleaneq8zz138hvwog', 'NRCNRCB4-DARK-60090914351_1_489_SE_2016-01-09T09h52m02_level1b_uncal.fits'),
                        ('https://stsci.box.com/s/ked1azkg05ia2qledmpm29mkiktinn3y', 'NRCNRCB4-DARK-60091316411_1_489_SE_2016-01-09T14h23m38_level1b_uncal.fits'),
                        ('https://stsci.box.com/s/ninym1sr7yrgb9tjmfczkb1vh6v2an0t', 'NRCNRCB4-DARK-60091822061_1_489_SE_2016-01-09T18h53m02_level1b_uncal.fits'),
                        ('https://stsci.box.com/s/y9psja8ol4kqvkqjx4z5hlo7cbqrpqp7', 'NRCNRCBLONG-DARK-60090141241_1_490_SE_2016-01-09T02h46m50_level1b_uncal.fits'),
                        ('https://stsci.box.com/s/7jj24l6i3k5yy23gclqvvs1gy8cqeiix', 'NRCNRCBLONG-DARK-60090535381_1_490_SE_2016-01-09T06h17m51_level1b_uncal.fits'),
                        ('https://stsci.box.com/s/56h3wdjro3ici53tbt6nivjc0ntxx8f3', 'NRCNRCBLONG-DARK-60090939281_1_490_SE_2016-01-09T10h22m25_level1b_uncal.fits'),
                        ('https://stsci.box.com/s/8wq3o6n8bgh448zpgz7801lnndzh24da', 'NRCNRCBLONG-DARK-60091338491_1_490_SE_2016-01-09T15h46m43_level1b_uncal.fits'),
                        ('https://stsci.box.com/s/bks6n8q83ocfremqn99jt8c5kn8niyid', 'NRCNRCBLONG-DARK-60101408431_1_490_SE_2016-01-10T15h01m09_level1b_uncal.fits')]
NIRCAM_LINEARIZED_DARK_URLS = [('https://stsci.box.com/s/dchmjjmepngpdo4xrabk8d5h1q63m3hf', 'Linearized_Dark_and_SBRefpix_NRCNRCA1-DARK-60082202011_1_481_SE_2016-01-09T00h03m58_uncal.fits'),
                               ('https://stsci.box.com/s/z5fp0yhy7hydb3m59yevgxif8b9rrg8f', 'Linearized_Dark_and_SBRefpix_NRCNRCA1-DARK-60090213141_1_481_SE_2016-01-09T02h53m12_uncal.fits'),
                               ('https://stsci.box.com/s/mqbwnwx8vjibgd50hahtd4i5qvc1mo0p', 'Linearized_Dark_and_SBRefpix_NRCNRCA1-DARK-60090604481_1_481_SE_2016-01-09T06h52m47_uncal.fits'),
                               ('https://stsci.box.com/s/dc0y3k95jo5pd3yhskig4bimvgfjkopl', 'Linearized_Dark_and_SBRefpix_NRCNRCA1-DARK-60091005411_1_481_SE_2016-01-09T10h56m36_uncal.fits'),
                               ('https://stsci.box.com/s/8j4jbzis927j74m6eizy90n0l5ukbd2g', 'Linearized_Dark_and_SBRefpix_NRCNRCA1-DARK-60091434481_1_481_SE_2016-01-09T15h50m45_uncal.fits'),
                               ('https://stsci.box.com/s/6h3uau1yr2sdb16xyn7dbfv83gmq1iaf', 'Linearized_Dark_and_SBRefpix_NRCNRCA2-DARK-60082224241_1_482_SE_2016-01-09T00h10m36_uncal.fits'),
                               ('https://stsci.box.com/s/re2lt2feyvyypj8pjn47tug8qlk1hzfm', 'Linearized_Dark_and_SBRefpix_NRCNRCA2-DARK-60090235001_1_482_SE_2016-01-09T04h17m03_uncal.fits'),
                               ('https://stsci.box.com/s/fszoeeviszj91li1v9amcfce68g7f5hz', 'Linearized_Dark_and_SBRefpix_NRCNRCA2-DARK-60090635511_1_482_SE_2016-01-09T07h05m19_uncal.fits'),
                               ('https://stsci.box.com/s/3gukyemqcjcqnt39f7s2sxyjlzcr7mk3', 'Linearized_Dark_and_SBRefpix_NRCNRCA2-DARK-60091030561_1_482_SE_2016-01-09T11h03m17_uncal.fits'),
                               ('https://stsci.box.com/s/via9puv3co1yeqg6vrqpsftxheer6m6d', 'Linearized_Dark_and_SBRefpix_NRCNRCA2-DARK-60091457131_1_482_SE_2016-01-09T15h50m45_uncal.fits'),
                               ('https://stsci.box.com/s/cnjlguana504waizgw15ez19lfgx3mwo', 'Linearized_Dark_and_SBRefpix_NRCNRCA3-DARK-60082245481_1_483_SE_2016-01-09T00h04m26_uncal.fits'),
                               ('https://stsci.box.com/s/2epggrnq3misb3zn8e7iys9sxxhgzrqt', 'Linearized_Dark_and_SBRefpix_NRCNRCA3-DARK-60090321241_1_483_SE_2016-01-09T04h17m10_uncal.fits'),
                               ('https://stsci.box.com/s/3dpeo1kwn4orhpgxdybm3qo830rlcvm9', 'Linearized_Dark_and_SBRefpix_NRCNRCA3-DARK-60090656591_1_483_SE_2016-01-09T07h31m27_uncal.fits'),
                               ('https://stsci.box.com/s/7nin41qwumemceb6ma3xurqycg4dde1w', 'Linearized_Dark_and_SBRefpix_NRCNRCA3-DARK-60091052561_1_483_SE_2016-01-09T11h28m06_uncal.fits'),
                               ('https://stsci.box.com/s/6yt605vznl90sjo41ny8lgwtdyhxzpu7', 'Linearized_Dark_and_SBRefpix_NRCNRCA3-DARK-60091522581_1_483_SE_2016-01-09T16h30m34_uncal.fits'),
                               ('https://stsci.box.com/s/5abqwlhau5cvgqtf7kinpgstqwx5tf7d', 'Linearized_Dark_and_SBRefpix_NRCNRCA4-DARK-60082307391_1_484_SE_2016-01-09T00h04m08_uncal.fits'),
                               ('https://stsci.box.com/s/1h86n0fcnmex8cfrjsl56hzdcjkbqaox', 'Linearized_Dark_and_SBRefpix_NRCNRCA4-DARK-60090259591_1_484_SE_2016-01-09T04h16m50_uncal.fits'),
                               ('https://stsci.box.com/s/wttboeuk25eaxovslkm1psckitmtdeuh', 'Linearized_Dark_and_SBRefpix_NRCNRCA4-DARK-60090720041_1_484_SE_2016-01-09T07h58m26_uncal.fits'),
                               ('https://stsci.box.com/s/acspa28skwaagjje74sairln2k61s37l', 'Linearized_Dark_and_SBRefpix_NRCNRCA4-DARK-60091117441_1_484_SE_2016-01-09T11h52m23_uncal.fits'),
                               ('https://stsci.box.com/s/l9171f1e8x3g8ichtu3w6gze6g8oo7ik', 'Linearized_Dark_and_SBRefpix_NRCNRCA4-DARK-60091548131_1_484_SE_2016-01-09T16h30m50_uncal.fits'),
                               ('https://stsci.box.com/s/8vrtbwiquazo3v0gis2ibd677ro5jw75', 'Linearized_Dark_and_SBRefpix_NRCNRCALONG-DARK-60082329041_1_485_SE_2016-01-09T00h04m16_uncal.fits'),
                               ('https://stsci.box.com/s/mk15yiw25jc6ucsg8f8hl9xya55wvcqz', 'Linearized_Dark_and_SBRefpix_NRCNRCALONG-DARK-60090344021_1_485_SE_2016-01-09T04h16m42_uncal.fits'),
                               ('https://stsci.box.com/s/f8ikd8ursxxmizh5i88rzz1frvg7n002', 'Linearized_Dark_and_SBRefpix_NRCNRCALONG-DARK-60090746381_1_485_SE_2016-01-09T08h21m48_uncal.fits'),
                               ('https://stsci.box.com/s/7zzdnsgrg5kddp067hv6umpztbzido1s', 'Linearized_Dark_and_SBRefpix_NRCNRCALONG-DARK-60091140151_1_485_SE_2016-01-09T14h23m49_uncal.fits'),
                               ('https://stsci.box.com/s/2djmrufvnbu014i1uilyphqbogcplj03', 'Linearized_Dark_and_SBRefpix_NRCNRCALONG-DARK-60091611271_1_485_SE_2016-01-09T17h16m35_uncal.fits'),
                               ('https://stsci.box.com/s/bebwkwderw0y4qhg342z5joyvbm3ddmu', 'Linearized_Dark_and_SBRefpix_NRCNRCB1-DARK-60082356471_1_486_SE_2016-01-09T02h47m00_uncal.fits'),
                               ('https://stsci.box.com/s/kbicf1i4lp4lv951lakxn7i5mak40jg2', 'Linearized_Dark_and_SBRefpix_NRCNRCB1-DARK-60090405201_1_486_SE_2016-01-09T05h33m56_uncal.fits'),
                               ('https://stsci.box.com/s/f7egrgol987bkev77cy5c63ljy4r0hv5', 'Linearized_Dark_and_SBRefpix_NRCNRCB1-DARK-60090807581_1_486_SE_2016-01-09T08h48m11_uncal.fits'),
                               ('https://stsci.box.com/s/ba0lgcegd8h3xormuc41wle2i4fr1p1e', 'Linearized_Dark_and_SBRefpix_NRCNRCB1-DARK-60091205311_1_486_SE_2016-01-09T14h30m08_uncal.fits'),
                               ('https://stsci.box.com/s/44chr1i2gyojtke34pboj7nyfh2mtmne', 'Linearized_Dark_and_SBRefpix_NRCNRCB1-DARK-60091636021_1_486_SE_2016-01-09T17h16m13_uncal.fits'),
                               ('https://stsci.box.com/s/8f01ir2s6lt6itisoypw3t2owvyajwno', 'Linearized_Dark_and_SBRefpix_NRCNRCB2-DARK-60090021181_1_487_SE_2016-01-09T02h51m54_uncal.fits'),
                               ('https://stsci.box.com/s/isrohgs3ekpt9a2qubojqwgt2vkefyxa', 'Linearized_Dark_and_SBRefpix_NRCNRCB2-DARK-60090427541_1_487_SE_2016-01-09T05h33m14_uncal.fits'),
                               ('https://stsci.box.com/s/vh5pv2as2nfzh3rgutuwdr9kw4iz0kwt', 'Linearized_Dark_and_SBRefpix_NRCNRCB2-DARK-60090830131_1_487_SE_2016-01-09T08h59m50_uncal.fits'),
                               ('https://stsci.box.com/s/p6ibgezka3vkvr5bsjv52xlvius925ff', 'Linearized_Dark_and_SBRefpix_NRCNRCB2-DARK-60091230011_1_487_SE_2016-01-09T14h23m47_uncal.fits'),
                               ('https://stsci.box.com/s/n94tmd71cgabs3dswsdodj1p65uwz0cw', 'Linearized_Dark_and_SBRefpix_NRCNRCB2-DARK-60091735131_1_487_SE_2016-01-09T18h09m45_uncal.fits'),
                               ('https://stsci.box.com/s/sb1xugk7cdq6zhqkb65ifbl5y1h3l8ob', 'Linearized_Dark_and_SBRefpix_NRCNRCB3-DARK-60090043151_1_488_SE_2016-01-09T02h53m21_uncal.fits'),
                               ('https://stsci.box.com/s/m5zqf0fqq5ycw9n0v5vageukk1v4wl9j', 'Linearized_Dark_and_SBRefpix_NRCNRCB3-DARK-60090451471_1_488_SE_2016-01-09T05h33m25_uncal.fits'),
                               ('https://stsci.box.com/s/gqkru1s8zwvrps3l4t31d1prk6f5r2b9', 'Linearized_Dark_and_SBRefpix_NRCNRCB3-DARK-60090852451_1_488_SE_2016-01-09T09h35m03_uncal.fits'),
                               ('https://stsci.box.com/s/upk0cqi9aqivj300ui2s8non2a5u3jlb', 'Linearized_Dark_and_SBRefpix_NRCNRCB3-DARK-60091254111_1_488_SE_2016-01-09T14h23m58_uncal.fits'),
                               ('https://stsci.box.com/s/lh7595afpjqvriwaajrqd9sm3i54zxhl', 'Linearized_Dark_and_SBRefpix_NRCNRCB3-DARK-60091757401_1_488_SE_2016-01-09T18h40m55_uncal.fits'),
                               ('https://stsci.box.com/s/pmmr6ozzxo4zgbxv7oqwg1xbyrze67mu', 'Linearized_Dark_and_SBRefpix_NRCNRCB4-DARK-60090118261_1_489_SE_2016-01-09T02h46m53_uncal.fits'),
                               ('https://stsci.box.com/s/nrui4vu3jgptopw812mgjf0pxjnjh95k', 'Linearized_Dark_and_SBRefpix_NRCNRCB4-DARK-60090513431_1_489_SE_2016-01-09T05h57m50_uncal.fits'),
                               ('https://stsci.box.com/s/faxxltcjpm45g2fugvd8ewu4kodm8a3z', 'Linearized_Dark_and_SBRefpix_NRCNRCB4-DARK-60090914351_1_489_SE_2016-01-09T09h52m02_uncal.fits'),
                               ('https://stsci.box.com/s/ll9n77ca9i8dz7ae41b9ae4hc1jlh5x6', 'Linearized_Dark_and_SBRefpix_NRCNRCB4-DARK-60091316411_1_489_SE_2016-01-09T14h23m38_uncal.fits'),
                               ('https://stsci.box.com/s/59u1h4sxthx2brm6ukaacbbcpa36wuhm', 'Linearized_Dark_and_SBRefpix_NRCNRCB4-DARK-60091822061_1_489_SE_2016-01-09T18h53m02_uncal.fits'),
                               ('https://stsci.box.com/s/mhy8m4sdhcfv4t5bkqbtn0sr8lzplsxo', 'Linearized_Dark_and_SBRefpix_NRCNRCBLONG-DARK-60090141241_1_490_SE_2016-01-09T02h46m50_uncal.fits'),
                               ('https://stsci.box.com/s/1t03er9udcj0fjacx1huhyx5qj8chjzv', 'Linearized_Dark_and_SBRefpix_NRCNRCBLONG-DARK-60090535381_1_490_SE_2016-01-09T06h17m51_uncal.fits'),
                               ('https://stsci.box.com/s/qmssc39jl1wm3bv2biiawha67xc17eiv', 'Linearized_Dark_and_SBRefpix_NRCNRCBLONG-DARK-60090939281_1_490_SE_2016-01-09T10h22m25_uncal.fits'),
                               ('https://stsci.box.com/s/q0sbu5lekvl1gk5u9wrvkhm3e74m7vfq', 'Linearized_Dark_and_SBRefpix_NRCNRCBLONG-DARK-60091338491_1_490_SE_2016-01-09T15h46m43_uncal.fits'),
                               ('https://stsci.box.com/s/0hf9nopvq0vk16oselokbnqo80wmf788', 'Linearized_Dark_and_SBRefpix_NRCNRCBLONG-DARK-60101408431_1_490_SE_2016-01-10T15h01m09_uncal.fits')]

NIRISS_RAW_DARK_URLS = [('https://stsci.box.com/s/1pr9cfwx2d8r6iju9afmhsylowtwq3x4', 'NISNIRISSDARK-153451235_11_496_SE_2015-12-11T16h05m20_dms_uncal.fits'),
                        ('https://stsci.box.com/s/cbnz7he6l9nva1lhrmn8pvz42hfb2ke5', 'NISNIRISSDARK-153451235_12_496_SE_2015-12-11T16h23m51_dms_uncal.fits'),
                        ('https://stsci.box.com/s/xxwjvy4w6hvmllkkzhdpydwk4hy9p997', 'NISNIRISSDARK-153451235_13_496_SE_2015-12-11T16h42m52_dms_uncal.fits'),
                        ('https://stsci.box.com/s/0a8xl3e6w45rw5s5xlnk4m0nkhx2nrgd', 'NISNIRISSDARK-153451235_14_496_SE_2015-12-11T17h01m50_dms_uncal.fits'),
                        ('https://stsci.box.com/s/jjax31gw1bxp4iiaeen4gk869yic3a9k', 'NISNIRISSDARK-153451235_15_496_SE_2015-12-11T17h20m40_dms_uncal.fits'),
                        ('https://stsci.box.com/s/rw04slw0ib53giuey7igysm6ge2hbzet', 'NISNIRISSDARK-153451235_16_496_SE_2015-12-11T17h40m30_dms_uncal.fits'),
                        ('https://stsci.box.com/s/n3geovm7mxn31f4piziqb89htu4ak1bu', 'NISNIRISSDARK-153451235_17_496_SE_2015-12-11T17h59m52_dms_uncal.fits'),
                        ('https://stsci.box.com/s/8ddnqcphujkncpg6niy1wgq5d5otlth1', 'NISNIRISSDARK-153451235_18_496_SE_2015-12-11T18h16m31_dms_uncal.fits'),
                        ('https://stsci.box.com/s/umituldjs916c5yhl0at8si29mg10qmq', 'NISNIRISSDARK-153451235_19_496_SE_2015-12-11T18h36m32_dms_uncal.fits'),
                        ('https://stsci.box.com/s/mbhyo8eqescy4v77gwznqd0aajk72wx2', 'NISNIRISSDARK-153451235_20_496_SE_2015-12-11T18h53m52_dms_uncal.fits'),
                        ('https://stsci.box.com/s/kh8ep1ecazy9fmw4we36kxg51e75hhzi', 'NISNIRISSDARK-172500017_13_496_SE_2017-09-07T04h48m22_dms_uncal.fits'),
                        ('https://stsci.box.com/s/1dc1q3f942gzjr76r81837tt6uyfh5qk', 'NISNIRISSDARK-172500017_14_496_SE_2017-09-07T05h06m42_dms_uncal.fits'),
                        ('https://stsci.box.com/s/dg2niytahewqpsepto1tl23q7u03b230', 'NISNIRISSDARK-172500017_15_496_SE_2017-09-07T05h28m22_dms_uncal.fits'),
                        ('https://stsci.box.com/s/99preol28qzhg7ctt0r4vsf8nrblcitt', 'NISNIRISSDARK-172500017_16_496_SE_2017-09-07T05h47m42_dms_uncal.fits'),
                        ('https://stsci.box.com/s/agtzclaccw93gobr76kqygvbs3xth0n2', 'NISNIRISSDARK-172500017_17_496_SE_2017-09-07T06h09m02_dms_uncal.fits'),
                        ('https://stsci.box.com/s/dr4hkbw15397iy93wmqcqr1mcxijdss5', 'NISNIRISSDARK-172500017_18_496_SE_2017-09-07T06h29m12_dms_uncal.fits'),
                        ('https://stsci.box.com/s/ebo2m6kaaqwvxu5rtnpiky6amt6k8733', 'NISNIRISSDARK-172500017_19_496_SE_2017-09-07T06h49m52_dms_uncal.fits'),
                        ('https://stsci.box.com/s/y0db7ckqj4y7cfhmkegphi3arxacews0', 'NISNIRISSDARK-172500017_20_496_SE_2017-09-07T07h09m22_dms_uncal.fits'),
                        ('https://stsci.box.com/s/3t3by35z9jhz1uz7su85rxwkw4j3812m', 'NISNIRISSDARK-172500017_21_496_SE_2017-09-07T07h29m52_dms_uncal.fits'),
                        ('https://stsci.box.com/s/5udxxbpnkda7fjpgc52wd9lv125gwt0i', 'NISNIRISSDARK-172500017_22_496_SE_2017-09-07T07h50m32_dms_uncal.fits')]
NIRISS_LINEARIZED_DARK_URLS = [('https://stsci.box.com/s/nte0e1k6mtmym50kqe5wlngg6ambm6j2', 'Linearized_Dark_and_SBRefpix_NISNIRISSDARK-153451235_17_496_SE_2015-12-11T17h59m52_dms_uncal_linear_dark_prep_object.fits'),
                               ('https://stsci.box.com/s/vif9ha3z70mf4x4ln70464o093qalbjs', 'Linearized_Dark_and_SBRefpix_NISNIRISSDARK-153451235_16_496_SE_2015-12-11T17h40m30_dms_uncal_linear_dark_prep_object.fits'),
                               ('https://stsci.box.com/s/by38gaqd2w8x3l0fmuox76dc26wj3ry2', 'Linearized_Dark_and_SBRefpix_NISNIRISSDARK-153451235_15_496_SE_2015-12-11T17h20m40_dms_uncal_linear_dark_prep_object.fits'),
                               ('https://stsci.box.com/s/ymee55dyp1dnarofrgk9inlgoo5c9lko', 'Linearized_Dark_and_SBRefpix_NISNIRISSDARK-153451235_14_496_SE_2015-12-11T17h01m50_dms_uncal_linear_dark_prep_object.fits'),
                               ('https://stsci.box.com/s/gvx1mjhqpmbtvpln3aiojfigsfflb2v3', 'Linearized_Dark_and_SBRefpix_NISNIRISSDARK-153451235_13_496_SE_2015-12-11T16h42m52_dms_uncal_linear_dark_prep_object.fits'),
                               ('https://stsci.box.com/s/cduow17sa0cejtdm28rh48um9mll9co0', 'Linearized_Dark_and_SBRefpix_NISNIRISSDARK-153451235_12_496_SE_2015-12-11T16h23m51_dms_uncal_linear_dark_prep_object.fits'),
                               ('https://stsci.box.com/s/0lb7f57m9iakhiuc6p22kc3okgtcj10q', 'Linearized_Dark_and_SBRefpix_NISNIRISSDARK-153451235_11_496_SE_2015-12-11T16h05m20_dms_uncal_linear_dark_prep_object.fits'),
                               ('https://stsci.box.com/s/tzlrfwwp7cwvnstc7h8h4zvtfidpqeyh', 'Linearized_Dark_and_SBRefpix_NISNIRISSDARK-153451235_18_496_SE_2015-12-11T18h16m31_dms_uncal_linear_dark_prep_object.fits'),
                               ('https://stsci.box.com/s/96pvv9yo3liew5tduij4t9egydwh7m81', 'Linearized_Dark_and_SBRefpix_NISNIRISSDARK-153451235_19_496_SE_2015-12-11T18h36m32_dms_uncal_linear_dark_prep_object.fits'),
                               ('https://stsci.box.com/s/1b8v1zugso34uu6gpvplcq19qclhazta', 'Linearized_Dark_and_SBRefpix_NISNIRISSDARK-153451235_20_496_SE_2015-12-11T18h53m52_dms_uncal_linear_dark_prep_object.fits'),
                               ('https://stsci.box.com/s/j76aa9m6qob2n4iix728o50ug738m0r3', 'Linearized_Dark_and_SBRefpix_NISNIRISSDARK-172500017_13_496_SE_2017-09-07T04h48m22_dms_uncal_linear_dark_prep_object.fits'),
                               ('https://stsci.box.com/s/0ncv03i5uhp6e97y8ofb31j3flzd5e87', 'Linearized_Dark_and_SBRefpix_NISNIRISSDARK-172500017_14_496_SE_2017-09-07T05h06m42_dms_uncal_linear_dark_prep_object.fits'),
                               ('https://stsci.box.com/s/w1lcdxo927qr6eq0pqx5eiit8iz5c3ae', 'Linearized_Dark_and_SBRefpix_NISNIRISSDARK-172500017_15_496_SE_2017-09-07T05h28m22_dms_uncal_linear_dark_prep_object.fits'),
                               ('https://stsci.box.com/s/3xf32m9k9t9daukblqpcjje2yj9mx10d', 'Linearized_Dark_and_SBRefpix_NISNIRISSDARK-172500017_16_496_SE_2017-09-07T05h47m42_dms_uncal_linear_dark_prep_object.fits'),
                               ('https://stsci.box.com/s/clud1dkupuxkkf77c96qbhdyfn0ukeop', 'Linearized_Dark_and_SBRefpix_NISNIRISSDARK-172500017_17_496_SE_2017-09-07T06h09m02_dms_uncal_linear_dark_prep_object.fits'),
                               ('https://stsci.box.com/s/nhrpau4kuxs0pm93orng1k6n6mh29m06', 'Linearized_Dark_and_SBRefpix_NISNIRISSDARK-172500017_18_496_SE_2017-09-07T06h29m12_dms_uncal_linear_dark_prep_object.fits'),
                               ('https://stsci.box.com/s/vjel9s4x44nqn55d8dsk9zauwq96tz3h', 'Linearized_Dark_and_SBRefpix_NISNIRISSDARK-172500017_19_496_SE_2017-09-07T06h49m52_dms_uncal_linear_dark_prep_object.fits'),
                               ('https://stsci.box.com/s/o52djwdwksvnjkl7xt0ndlnjpfa6tlms', 'Linearized_Dark_and_SBRefpix_NISNIRISSDARK-172500017_20_496_SE_2017-09-07T07h09m22_dms_uncal_linear_dark_prep_object.fits'),
                               ('https://stsci.box.com/s/857olzwa1e51b05uz2bx6c13hzsufilz', 'Linearized_Dark_and_SBRefpix_NISNIRISSDARK-172500017_21_496_SE_2017-09-07T07h29m52_dms_uncal_linear_dark_prep_object.fits'),
                               ('https://stsci.box.com/s/isnevg8m2j58qrb72u19pp43k5rpksy1', 'Linearized_Dark_and_SBRefpix_NISNIRISSDARK-172500017_22_496_SE_2017-09-07T07h50m32_dms_uncal_linear_dark_prep_object.fits')]

# For testing
NIRISS_RAW_DARK_URLS = [('https://stsci.box.com/s/1pr9cfwx2d8r6iju9afmhsylowtwq3x4', 'NISNIRISSDARK-153451235_11_496_SE_2015-12-11T16h05m20_dms_uncal.fits')]
NIRISS_LINEARIZED_DARK_URLS = [('https://stsci.box.com/s/nte0e1k6mtmym50kqe5wlngg6ambm6j2', 'Linearized_Dark_and_SBRefpix_NISNIRISSDARK-153451235_17_496_SE_2015-12-11T17h59m52_dms_uncal_linear_dark_prep_object.fits')]


FGS_RAW_DARK_URLS = [('https://stsci.box.com/s/2nhm4pajg1d3b3vmj8p5wtsevxq41qsj', '29722_1x88_FGSF03512-D-NR-G2-5339214947_1_498_SE_2015-12-05T22h27m19_dms_uncal.fits'),
                     ('https://stsci.box.com/s/yq0pvyur651h8v1fz9t5wronvtbhv76b', '29782_1x88_FGSF03872-PAR-5340074326_1_498_SE_2015-12-06T12h22m47_dms_uncal.fits'),
                     ('https://stsci.box.com/s/72byn3psj6g3oawh3kp6fx5szfy1ahfs', '29813_1x88_FGSF037221-MR-2-5340161743_1_498_SE_2015-12-06T16h45m10_dms_uncal.fits'),
                     ('https://stsci.box.com/s/kqp2rmgff8esq2dyi5zeduaayunyhgtz', '30632_1x88_FGSF03511-D-NR-G1-5346180117_1_497_SE_2015-12-12T19h00m12_dms_uncal.fits'),
                     ('https://stsci.box.com/s/j3nlgllcmsmi8wtxo5kewzb7wvrefq0i', '30670_1x88_FGSF03511-D-NR-G2-5346181816_1_498_SE_2015-12-12T21h31m01_dms_uncal.fits'),
                     ('https://stsci.box.com/s/of8p9yk3jeo8hmi3k91wi4gk9kol8vlo', '30742_1x88_FGSF03871-PAR-5347035139_1_498_SE_2015-12-13T05h23m30_dms_uncal.fits'),
                     ('https://stsci.box.com/s/54ggqqbf2ltnfy0efed5d2othk4sf0rv', '30749_1x88_FGSF03881-PAR-5347043800_1_497_SE_2015-12-13T09h02m01_dms_uncal.fits'),
                     ('https://stsci.box.com/s/2iilllsjo54yj7g8m6d931u19aforcbf', '30829_1x88_FGSF037111-G1NRNC-5347151640_1_497_SE_2015-12-13T16h28m38_dms_uncal.fits')]
FGS_LINEARIZED_DARK_URLS = [('https://stsci.box.com/s/6y0rsqgongmyp9cffqwd6k2k3ivl6pjf', '29722_1x88_FGSF03512-D-NR-G2-5339214947_1_498_SE_2015-12-05T22h27m19_dms_uncal_linearized.fits'),
                            ('https://stsci.box.com/s/t7xyd85wcvvxgzaeh26wlmstmp437g39', '29782_1x88_FGSF03872-PAR-5340074326_1_498_SE_2015-12-06T12h22m47_dms_uncal_linearized.fits'),
                            ('https://stsci.box.com/s/y5dr624wwc3rf7iadc51dblw9vn5bavf', '29813_1x88_FGSF037221-MR-2-5340161743_1_498_SE_2015-12-06T16h45m10_dms_uncal_linearized.fits'),
                            ('https://stsci.box.com/s/xg35tec3ohaeihmp1qpiktur2y9lnfem', '30632_1x88_FGSF03511-D-NR-G1-5346180117_1_497_SE_2015-12-12T19h00m12_dms_uncal_linearized.fits'),
                            ('https://stsci.box.com/s/0rkd1vzphgqzjl8yinusck4c57dm5nov', '30670_1x88_FGSF03511-D-NR-G2-5346181816_1_498_SE_2015-12-12T21h31m01_dms_uncal_linearized.fits'),
                            ('https://stsci.box.com/s/4xe1mmap18612b57joctwo20t38ald95', '30742_1x88_FGSF03871-PAR-5347035139_1_498_SE_2015-12-13T05h23m30_dms_uncal_linearized.fits'),
                            ('https://stsci.box.com/s/jq206o2pm5ydud1xidxyurcf74zwuzb2', '30749_1x88_FGSF03881-PAR-5347043800_1_497_SE_2015-12-13T09h02m01_dms_uncal_linearized.fits'),
                            ('https://stsci.box.com/s/kai7ms09pvbfm5zdr079gss27ki3j6qd', '30829_1x88_FGSF037111-G1NRNC-5347151640_1_497_SE_2015-12-13T16h28m38_dms_uncal_linearized.fits')]


def download_file(url, file_name, output_directory='./'):
    """Download into the current working directory the
    file from Box given the direct URL

    Parameters
    ----------
    url : str
        URL to the file to be downloaded

    Returns
    -------
    download_filename : str
        Name of the downloaded file
    """
    with requests.get(url, stream=True) as response:
        if response.status_code != 200:
            raise RuntimeError("Wrong URL - {}".format(url))
        download_filename = os.path.join(output_directory, file_name)
        with open(download_filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=2048):
                if chunk:
                    f.write(chunk)
    return download_filename


def download_reffiles(directory, instrument='all', psf_version='subpix', dark_type='linearized'):
    """Download tarred and gzipped reference files. Expand, unzip and
    organize into the necessary directory structure such that Mirage
    can use them.

    Parameters
    ----------
    directory : str
        Directory into which the reference files are placed. This will
        be the directory set to the MIRAGE_DATA environment variable

    instrument : str
        If ``all``: download all files. If the name of an individual
        instrument, download only the data for that instrument

    psf_version : str
        If ``gridded``: download new PSf library
        If ``something else``: download old PSF library

    dark_type : str
        Type of dark current files to download. Options are:
        'linearized': download linearize dark current ramps
        'raw': download raw dark current ramps
        'both': download both raw and linearized dark current ramps
    """
    file_list = get_file_list(instrument.lower(), psf_version.lower(), dark_type.lower())

    for file_info in file_list:
        file_url, filename = file_info
        print('Downloading: {}'.format(filename))
        download_file(file_url, filename, directory)
        local_file = os.path.join(directory, filename)

        # Unzip and untar file
        if 'tar.gz' in local_file:
            print('Unzipping/extracting {}'.format(filename))
            file_object = tarfile.open(name=local_file, mode='r:gz', )
            file_object.extractall(path=directory)
        else:
            # Darks need to be unzipped into the correct directory
            if 'linearized' in filename.lower():
                cal = 'linearized'
            else:
                cal = 'raw'

            # Determine directory
            if 'NRCNRC' in filename:
                det_str = filename.split('NRCNRC')[1].split('-')[0]
                if 'LONG' in det_str:
                    det_str.replace('LONG', '5')
                darks_dir = os.path.join(directory, 'mirage_data', 'nircam', 'darks')
                sub_directory = os.path.join(directory, 'mirage_data', 'nircam', 'darks', cal, det_str)
            elif 'niriss' in filename.lower():
                sub_directory = os.path.join(directory, 'mirage_data', 'niriss', 'darks', cal)
            elif 'fgs' in filename:
                sub_directory = os.path.join(directory, 'mirage_data', 'niriss', 'darks', cal)

            # Create the directory if it does not yet exist
            ensure_dir_exists(darks_dir)
            ensure_dir_exists(os.path.join(darks_dir, cal))
            ensure_dir_exists(sub_directory)

            final_location = os.path.join(sub_directory, filename)

            # Move the zipped file into the correct subdirectory
            # and unzip
            print('Moving {} to {}'.format(filename, sub_directory))
            shutil.move(local_file, final_location)
            print('Unzipping {}'.format(filename))
            unzip_file(final_location, sub_directory)

    print(('Mirage reference files downloaded and extracted. Before '
           'using Mirage, be sure to set the MIRAGE_DATA environment '
           'variable to point to {}/mirage_data'.format(directory)))
    print('\n In bash: ')
    print('export MIRAGE_DATA="{}"'.format(os.path.join(directory, 'mirage_data')))


def get_file_list(instruments, library_version, dark_current):
    """Collect the list of URLs corresponding to the Mirage reference
    files to be downloaded

    Parameters
    ----------
    instruments : list
        List of instrument names for which to download data

    library_version : str
        Version of the PSF librarry to download.
        If ``gridded``: download PSf library that uses griddedPSFModels
        If ``something else``: download PSF library composed of
        individual fits files

    dark_current : str
        Type of dark current files to download. Options are:
        'linearized': download linearize dark current ramps
        'raw': download raw dark current ramps
        'both': download both raw and linearized dark current ramps

    Returns
    -------
    urls : list
        List of tuples. Each tuple contains:
        (URL for downloading, name of file)
    """
    urls = []
    instrument_names = [name.strip().lower() for name in instruments.split(',')]

    if 'all' in instrument_names:
        instrument_names = ['nircam', 'niriss', 'fgs']

    for instrument_name in instrument_names:
        # NIRCam
        if instrument_name.lower() == 'nircam':
            urls.extend(NIRCAM_REFFILES_URL)
            urls.extend(NIRCAM_CR_LIBRARY_URL)

            if library_version == 'gridded':
                urls.extend(NIRCAM_GRIDDED_PSF_URLS)
            else:
                urls.extend(NIRCAM_INDIVIDUAL_PSF_URLS)

            if dark_current in ['linearized', 'both']:
                urls.extend(NIRCAM_LINEARIZED_DARK_URLS)
            elif dark_current in ['raw', 'both']:
                urls.extend(NIRCAM_RAW_DARK_URLS)

        # NIRISS
        elif instrument_name.lower() == 'niriss':
            urls.extend(NIRISS_REFFILES_URL)
            urls.extend(NIRISS_CR_LIBRARY_URL)

            if library_version == 'gridded':
                urls.extend(NIRISS_GRIDDED_PSF_URLS)
            else:
                urls.extend(NIRISS_INDIVIDUAL_PSF_URLS)

            if dark_current in ['linearized', 'both']:
                urls.extend(NIRISS_LINEARIZED_DARK_URLS)
            elif dark_current in ['raw', 'both']:
                urls.extend(NIRISS_RAW_DARK_URLS)

        # FGS
        elif instrument_name.lower() == 'fgs':
            urls.extend(NIRISS_REFFILES_URL)
            urls.extend(NIRISS_CR_LIBRARY_URL)

            if library_version == 'gridded':
                urls.extend(FGS_GRIDDED_PSF_URLS)
            else:
                urls.extend(FGS_INDIVIDUAL_PSF_URLS)

            if dark_current in ['linearized', 'both']:
                urls.extend(FGS_LINEARIZED_DARK_URLS)
            elif dark_current in ['raw', 'both']:
                urls.extend(FGS_RAW_DARK_URLS)
    return urls


def unzip_file(filename, dir_name):
    """Unzip a file

    Parameters
    ----------
    filename : str
        Name of file to unzip

    dir_name : str
        Directory into which the file is unzipped
    """
    zip_ref = zipfile.ZipFile(filename, 'r')
    zip_ref.extractall(dir_name)
    zip_ref.close()
