]

# ------------------------------

1$draw=$1$len!:$1@$0!
$call_n=($1:$0+2$!)
1$push_array=$1$len!:$1@$0

1$len=0$1$_len!
2$_len=[$1@$2?$1+1$2$_len!b $1]

$newline={6yv 6*.4x>}
$space={>>}

# ------------------------------

$hr1={1x4>}
$hr2={1x2>}
$hr3={3x4>}
$hr4={>}
$hu2={^^ 1x8>}
$hu1={^ 1x4>}
$hd4={vvvv 1x4>}
$d2r=v{2x3vv>}{1x3>}s
$d4r=v{2x3vvvv>}{2x3>}s
$rd2d=[2x3 >{>vv}{v}s]
$rd4d=[2x3 >{>vvvv}{v}s]
$d4j=v{vvvv}{1x2<}s
$u2j=^{^^ 1x2<}{1x2<}s{1x2>}
$d2d=M{1x4>vv}C
$d4d=M{1x4>vvvv}C
$ru2r={2x3>}{^^>}{2x3>}s
$r2u2r={3x2>}{3x2^^>}{2x3>}s
$ru1u={1x3>}{2x4>^}{1y2^}s
$r1u1u={1x6>}{1x4>^}{1y2^}s
$r2u1u={2x3>}{>^}{1y2^}s
$ru2u={1x3>}{>^^}{^}s
$r1u2u=[1x2 {1x3>}{>^^}{^}s]
$r2u2u={2x3>}{4x3>^^}{^}s
$ru4u={>}{2x3>^^^^}{^}s
$r1u4u=[1x2 {2x3>}{2x3>^^^^}{^}s]
$uru2ru={3y4^}{5x12>^^}{3y4^}s
$uru4ru={3y2^}{1x2>^^^^}{3y2^}s
$uu2r=[2x3 {^}{^^>}>s]
$uu4r=[2x3 {^}{^^^^>}{3x2>}s]
$rd2r={2x3>}{vv>}{2x3>}s

# ------------------------------

$chr_3_=
    $ru2r,
    $diacr,
    $rd2d,
    $uru2ru,
    $d2r

$chr_2_=
    $ru2u,
    $diac,
    $d2d,
    $uru2ru,
    $d2r

$detail_1_end=v{vv}{1x2<}s
$chr_1_=
    $ru2u,
    $diac,
    $detail_1_end

$detail_6_end={2x3>}{1x3>vv}{2x3<}s
$chr_6_=
    $ru2r,
    $diac,
    $detail_6_end

$detail_5_mid=[1.4x
    ({1.2y^}{.9y^>}{.15y 1x8>v}s)
    {0.7yv}{0.5xv>}{1x4>}s
    {0.5x>}{1.9y .5x>^}{0.5y^}s
]
$detail_5_end=[.95y$d2r!]
$chr_5_=
    $ru1u,
    $detail_5_mid,
    $diacl,
    $detail_5_end

$detail_4_mid={3x4^>}
$detail_4_end={<}{vv}{>}s
$chr_4_=
    $ru1u,
    $detail_4_mid,
    $diacl,
    $detail_4_end

$chr_9_=
    $ru2r,
    $diacr,
    $rd2d,
    $uu2r,
    $rd2r

$chr_8_=
    $ru2u,
    $diacr,
    $d2d,
    $uu2r,
    $rd2r

$detail_7_start=[
    {1x3>}{1x2^>}{1y2^}s
    ^{^>}{>}s
]
$detail_7_start_up=[
    ^
    ^{^>}{>}s
]
$detail_7_end={1x2<}{1x4vv>}>s
$chr_7_=
    $detail_7_start,
    $diacl,
    $detail_7_end

# ------------------------------

$chr_13j=
    $ru2r,
    $diacr,
    $rd2d,
    $uru2ru,
    $d4j,
    $hu2


$chr_12dw_=
    $ru2u,
    $diac,
    $d4d,
    $uru4ru,
    $d2r
$chr_12up1_=
    $ru4u,
    $d4d,
    $uru2ru,
    $diac,
    $d2r
$chr_12up2_=
    $ru2u,
    $diac,
    $d2d,
    $uru4ru,
    $d4r

$chr_11j=
    $ru2u,
    $diac,
    $d4j,
    $hu2


$detail_16_end={1x2>}{1x8vv>}{1x3<}s
$chr_16j=
    $ru2r,
    $diac,
    $detail_6_end,
    $detail_16_end,
    $hu2

$detail_15_end=[.975y$d4j!]
$chr_15j=
    $ru1u,
    $detail_5_mid,
    $diacl,
    $detail_15_end,
    $hu2
$detail_15v2_d_end=[1/.95y$u2j!]
$chr_15d=
    $ru1u,
    $detail_5_mid,
    $diacl,
    $detail_15v2_d_end,
    $hd4

$detail_14_mid1={1.2y^}{.9y^>}{.15y 1x8>v}s{0.1y^}
$detail_14_mid2={<v}{v}{v>}{1x4>}s
$chr_14_=
    $ru1u,
    $detail_14_mid1,
    $diac,
    $detail_14_mid2,
    $detail_16_end,
    $hu2

$detail_19_end=[
    {>}{vvvv1x2>}{1x2<}s
    {1x8>}
]

$chr_19j=
    $ru2r,
    $diac,
    $rd2d,
    $uu2r,
    $detail_19_end,
    $hu2

$chr_18_=
    $ru2u,
    $diac,
    $d4d,
    $uu4r,
    $rd2r

$detail_17_end={<}{1x4vvvv<<}{2x3<}s
$chr_17j=
    $detail_7_start,
    $diacl,
    $detail_17_end,
    $hu2

# ------------------------------

$diac=b
$diacl=b
$diacr=b

$acute=(
    {2y3^ 1x6<}
    M{1z2 >^}C
)
$_dot=[1r8 1z8 4:^1l4]
$dot=({2y3^} $_dot!)
$trema=({2y3^ 1x3<} $_dot! {2x3>} $_dot!)
$dotl=({1x2<}$dot!)
$dotr=({1x2>}$dot!)
$tremal=({1x2<}$trema!)
$tremar=({1x2>}$trema!)
$barl=({2y3^}<)
$barr=({2y3^}>)
$bar=({2y3^ 2x3<}>)

# ------------------------------

$chr_i_=$ru2u,$d2r

$chr_u_=$chr_i_!$chr_i_!

# ------------------------------

$sub_dn=
    $hd4,$ru2r,0,
    $hd4,$hr1,$uu2r
$sub_di=
    $hd4,$ru2u,0,
    $hd4,$r1u2u
$sub_dl=
    $hd4,$ru4u,0,
    $hd4,$r1u4u

$sub_jn=
    $hu2,$ru2r,0,
    $hu2,$hr2,$uu2r
$sub_j7=
    $hu2,$detail_7_start,0,
    $hu2,$hr2,$detail_7_start_up


$sub_j2i=
    $hu2,$ru2u,0,
    $hu2,$hr2,$r1u2u

$sub_jd4=
    $hu2,$hr2,$r1u2u,$d4d,0,
    $hu2,$hr2,$hu2,$d4d

$sub_j4=
    $hu2,$ru1u,0,
    $hu2,$hr2,$r1u1u

$sub_j2l=
    $hu2,$ru4u,0,
    $hu2,$hr2,$uru4ru


$sub_1i=
    $detail_1_end,$ru2u,0,
    $detail_1_end,$r2u2u
$sub_14=
    $detail_1_end,$ru1u,0,
    $detail_1_end,$r2u1u
$sub_1n=
    $detail_1_end,$ru2r,0,
    $detail_1_end,$r2u2r

$sub_6i=
    $detail_6_end,$ru2u,0,
    $detail_6_end,$r2u2u
