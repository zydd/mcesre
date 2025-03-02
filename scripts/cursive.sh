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
$hu2={^^}
$hu1={^}
$hd4={vvvv}
$d2r=v{2x3vv>}{1x3>}s
$d4r=v{2x3vvvv>}{2x3>}s
$rd2d=[2x3 >{>vv}{v}s]
$rd4d=[2x3 >{>vvvv}{v}s]
$d4j=v{vvvv}{1x2<}s
$u2j=^{^^ 1x2<}{1x2<}s{1x2>}
$d2d=M{1x4>vv}C
$d4d=M{1x4>vvvv}C
$ru2r={2x3>}{^^>}{2x3>}s
$r2u2r={3x2>}{3x2^^>}{>}s
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

$chr_3=
    $ru2r,
    $diacr,
    $rd2d,
    $uru2ru,
    $d2r

$chr_2=
    $ru2u,
    $diac,
    $d2d,
    $uru2ru,
    $d2r

$detail_1_end=v{vv}{1x2<}s
$chr_1=
    $ru2u,
    $diac,
    $detail_1_end

$detail_6_end={2x3>}{1x3>vv}{2x3<}s
$chr_6=
    $ru2r,
    $diac,
    $detail_6_end

$detail_5_begin=[1.4x $detail_4_mid!]
$detail_5_mid=[1.4x
    {<v}
    {0.7yv}{0.5xv>}{1x4>}s
    {0.5x>}{1.9y .5x>^}{0.5y^}s
]
$detail_5_end=[.95y$d2r!]
$chr_5=
    $ru1u,
    $detail_5_begin,
    $diacl,
    $detail_5_mid,
    $detail_5_end

$detail_4_mid={1.2y^}{.9y^>}{.15y 1x8>v}s{0.1y^}
$detail_4_end={<v}{v}{v>}{1x4>}s
$chr_4=
    $ru1u,
    $detail_4_mid,
    $diacl,
    $detail_4_end

$chr_9=
    $ru2r,
    $diacr,
    $rd2d,
    $uu2r,
    $rd2r

$chr_8=
    $ru2u,
    $diacr,
    $d2d,
    $uu2r,
    $rd2r

$detail_7_start=[
    {1x3>}{1x2^>}{1y2^}s
    ^{7x6^>}{7x6>}s
]
$detail_7_start_x2=[
    {2x3>}{^>}{1y2^}s
    ^{7x6^>}{7x6>}s
]
$detail_7_start_up=[
    ^
    ^{7x6^>}{7x6>}s
]
$detail_7_end={1x2<}{1x4vv>}>s
$chr_7=
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


$chr_12dw=
    $ru2u,
    $diac,
    $d4d,
    $uru4ru,
    $d2r
$chr_12up1=
    $ru4u,
    $d4d,
    $uru2ru,
    $d2r
$chr_12up2=
    $ru2u,
    $d2d,
    $uru4ru,
    $d4r

$chr_11j=
    $ru2u,
    $diac,
    $d4j,
    $hu2


$detail_16_end={1x2>}{vv}{1x3<}s
$chr_16j=
    $ru2r,
    $diac,
    $detail_6_end,
    $detail_16_end,
    $hu2

$detail_15_end=[.975y$d4j!]
$chr_15j=
    $ru1u,
    $detail_5_begin,
    $diacl,
    $detail_5_mid,
    $detail_15_end,
    $hu2
$detail_15v2_d_end=[1/.95y$u2j!]
$chr_15d=
    $ru1u,
    $detail_5_begin,
    $diacl,
    $detail_5_mid,
    $detail_15v2_d_end,
    $hd4

$chr_14j=
    $ru1u,
    $detail_4_mid,
    $diacl,
    $detail_4_end,
    $detail_16_end,
    $hu2
$detail_14_mid=({vv 1y2v} {v}{6y4v 1x4<}{1x4<}s)
$chr_14=
    $ru1u,
    $detail_4_mid,
    $diacl,
    $detail_14_mid,
    $detail_4_end

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

$chr_18j=
    $ru2u,
    $diac,
    $d2d,
    $uu2r,
    $detail_19_end,
    $hu2

$detail_17_end={<}{1x4vvvv<<}{2x3<}s
$chr_17j=
    $detail_7_start,
    $diacl,
    $detail_17_end,
    $hu2

# ------------------------------

$diac=b
$diacl={1x2<}
$diacr={1x2>}

$_dot=[1r8 1z8 4:^1l4]
$dot=({2y3^} $_dot!)
$bar=({2y3^ 2x3<}>)
$trema=({2y3^ 1x3<} $_dot! {2x3>} $_dot!)
$acute=({2y3^ 1x6<} M{1z2 ^>}C)
$grave=({2y3^ 1x6<} M{1z2 <^}C)
$caron=({2y3^ 1x6<} 1z2 (M{<^}C) M{^>}C)
$hat=({2y3^ 1x6<} 1z2 {>} (M{<^}C) {<<} (M{^>}C))

# ------------------------------

$prefix_i=$ru2u,$d2r

$prefix_u=$prefix_i!$prefix_i!

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
    $hu2,$hr3,$uu2r
$sub_j7=
    $hu2,$detail_7_start,0,
    $hu2,$hr3,$detail_7_start_up


$sub_j2i=
    $hu2,$ru2u,0,
    $hu2,$hr3,$r1u2u

$sub_jd4=
    $hu2,$hr2,$r1u2u,$d4d,0,
    $hu2,$hr3,$hu2,$d4d

$sub_j4=
    $hu2,$ru1u,0,
    $hu2,$hr3,$r1u1u

$sub_j2l=
    $hu2,$ru4u,0,
    $hu2,$hr3,$uru4ru


$sub_1i=
    $detail_1_end,$ru2u,0,
    $detail_1_end,$r2u2u
$sub_14=
    $detail_1_end,$ru1u,0,
    $detail_1_end,$r2u1u
$sub_17=
    $detail_1_end,$detail_7_start,0,
    $detail_1_end,$detail_7_start_x2
$sub_1n=
    $detail_1_end,$ru2r,0,
    $detail_1_end,$r2u2r


$sub_6i=
    $detail_6_end,$ru2u,0,
    $detail_6_end,$r2u2u
$sub_6n=
    $detail_6_end,$ru2r,0,
    $detail_6_end,$r2u2r
$sub_67=
    $detail_6_end,$detail_7_start,0,
    $detail_6_end,$detail_7_start_x2



$detail_lig_n1_end={1x3>}{1x3>vv}{1x2<}s
$detail_lig_51_end=[.95y$detail_1_end!]

$lig_2_1=$chr_2!P$chr_1+1!
$lig_3_1=$chr_3!P$chr_1+1!
$lig_5_1=$chr_5!P$detail_lig_51_end
$lig_7_1=$chr_7!P$chr_1+1!
$lig_8_1=$chr_8!P$chr_6+1!
$lig_9_1=$chr_9!P$chr_6+1!

$detail_lig_56_end=[{.925yv .05x<} 2x3 {1y2^ .1x>}{^>}>s]$detail_6_end!
$lig_2_6=$chr_2!P$d2d$uu2r$chr_6+1!
$lig_3_6=$chr_3!P$d2d$uu2r$chr_6+1!
$lig_5_6=$chr_5!P$detail_lig_56_end
$lig_8_6=$chr_8!P$rd2d$uu2r$chr_6+1!
$lig_8_16=$chr_8!P$rd2d$uu2r$chr_16j+1!
$lig_9_6=$chr_9!P$rd2d$uu2r$chr_6+1!
$lig_9_16=$chr_9!P$rd2d$uu2r$chr_16j+1!

$group_lig11=$chr_2,$chr_3,$chr_5,$chr_7,$chr_8,$chr_9
$group_lig11x1=$chr_11j
2$prod_lig11_lig11x1=$1!$chr_1!


$lig_12up1_1=$chr_12up1!P$detail_1_end
$lig_12dw_1=$chr_12dw!P$detail_1_end
$lig_12up1_11=$chr_12up1!$chr_1!
$lig_12dw_11=$chr_12dw!$chr_1!

$group_12dw=$chr_12dw
$group_s0=$chr_3,$chr_6,$chr_9,$chr_13j,$chr_16j,$chr_19j
2$prod_12dw_s0=$chr_12dw!PP$uu4r$2+1!

$lig_12dw_8=$chr_12dw!P$chr_8+1!
$lig_12dw_18=$chr_12dw!P$chr_18j+1!

$lig_12_6=$chr_12up1!PP$uu2r$chr_6+1!
$lig_12_16=$chr_12up1!PP$uu2r$chr_16j+1!

$detail_lig_12dw_4={3y2^}{1x8>^^^}{9y8^}s
$lig_12dw_4=$chr_12dw!PP$detail_lig_12dw_4$chr_4+1!
$lig_12dw_14=$chr_12dw!PP$detail_lig_12dw_4$chr_14j+1!

$lig_12dw_5=$chr_12dw!PP$detail_lig_12dw_4$chr_5+1!
$lig_12dw_15j=$chr_12dw!PP$detail_lig_12dw_4$chr_15j+1!
$lig_12dw_15d=$chr_12dw!PP$detail_lig_12dw_4$chr_15d+1!

$detail_lig_12dw_7={4.2y^}{4y^ 7x6>}{7x6>}s
$lig_12dw_7=$chr_12dw!PP$detail_lig_12dw_7$chr_7+1!
$lig_12dw_17=$chr_12dw!PP$detail_lig_12dw_7$chr_17j+1!


$lig_8_7=$chr_8!PP$detail_7_start_up$chr_7+1!
$lig_8_17=$chr_8!PP$detail_7_start_up$chr_17j+1!
$group_g8=$chr_8
2$prod_g8_s0=$chr_8!P$2+1!
2$prod_g8_c0=$1!PP$hu1$2+1!
2$prod_g8_a0=$1!PP$hu1$2+1!
# TODO: 86, 891 ambiguity


$lig_9_3=$chr_9!PPP$rd2d$uu2r$chr_3+1!
$lig_9_13=$chr_9!PPP$rd2d$uu2r$chr_13j+1!
$lig_9_7=$chr_9!PP$detail_7_start_up$chr_7+1!
$lig_9_17=$chr_9!PP$detail_7_start_up$chr_17j+1!
$group_g9=$chr_9
2$prod_g9_c0=$1!PP$hu1$2+1!
2$prod_g9_a0=$1!PP$hu1$2+1!

# $group_0j=$chr_11j,$chr_13j,$chr_15j,$chr_16j,$chr_17j,$chr_18j,$chr_19j
# $group_i0=$chr_1,$chr_2,$chr_8,$chr_11j,$chr_12up2,$chr_18j
# 2$prod_0j_i0=$1!$hr3$r1u2u$2+1!

# $group_n0=$chr_3,$chr_6,$chr_9
# 2$prod_0j_n0=$1!$hr3$uu2r$2+1!

$group_c0=$chr_4,$chr_14,$chr_14j
$group_a0=$chr_5,$chr_15d,$chr_15j
# 2$prod_0j_c0=$1!$hr2$r1u1u$2+1!
# 2$prod_0j_a0=$1!$hr3$hu1$2+1!

# $group_lig7=$chr_7
# $detail_lig7={4.2y^}{4y^>}{>}s
# 2$prod_0j_lig7=$1!$hr3$detail_7_start_up$chr_7+1!
