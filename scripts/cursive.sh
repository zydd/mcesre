
.4i
(9:$set_1@$0$draw!{>})
$newline!

(9:$set_2@$0$draw!{>})
$newline!

# (9:$set_3@$0$draw!{>})
# $newline!

$chr_i22_$draw!

# ($set_1@8$draw! $set_1@0$draw! {>} $chr_i_!$chr_i_! $chr_13j$draw!)

]

# ------------------------------

1$draw=$1$len!:$1@$0!
$call_n=($1:$0+2$!)
1$push_array=$1$len!:$1@$0

1$len=0$1$_len!
2$_len=[$1@$2?$1+1$2$_len!b $1]

$newline={5yv 5*.4x>}
$space={>>}

# ------------------------------

$u1={2x6>}{2x4>^}{1y2^}s
$u2={2x6>}{2x3>^^}{^}s
$uu2=[2x3 {^}{^^>}>s]
$uc2={3y4^}{5x12>^^}{3y4^}s
$d2=v{2x3vv>}{2x6>}s
$dd2=[2x3 >{>vv}{v}s]
$dl2={1x4>vv}C
$s2={2x3>}{^^>}{2x3>}s
$z2={2x3>}{vv>}{2x3>}s

$set_1=$chr_1_,$chr_2_,$chr_3_,$chr_4_,$chr_5_,$chr_6_,$chr_7_,$chr_8_,$chr_9_
$set_2=$chr_11j,$chr_12_,$chr_13j,$chr_14_,$chr_15j,$chr_16j,$chr_17j,$chr_18_,$chr_19j
$set_3=$chr_21_,$chr_22_,$chr_23_,$chr_24_,$chr_25_,$chr_26_,$chr_27_,$chr_28_,$chr_29_

# ------------------------------

$chr_3_=
    $s2,
    $dd2,
    $uc2,
    $d2,
    0

$chr_2_=
    $u2,
    $dl2,
    $uc2,
    $d2,
    0

$detail_1_end=v{vv}{1x2<}s

$chr_1_=
    $u2,
    $detail_1_end,
    0

$detail_6_end={2x3>}{1x3>vv}{2x3<}s

$chr_6_=
    $s2,
    $detail_6_end,
    0

$detail_5_mid=[1.4x
    ({1.2y^}{.9y^>}{.15y 1x8>v}s)
    {0.7yv}{0.5xv>}{1x4>}s
    {0.5x>}{1.9y .5x>^}{0.5y^}s
]

$detail_5_end=[.95y$d2!]

$chr_5_=
    $u1,
    $detail_5_mid,
    $detail_5_end,
    0

$detail_4_end=[
    ({1.2y^}{.9y^>}{.15y 1x8>v}s)
    {v}{1x2v>>}{1x4>}s
]

$chr_4_=
    $u1,
    $detail_4_end,
    0

$chr_9_=
    $s2,
    $dd2,
    $uu2,
    $z2,
    0

$chr_8_=
    $u2,
    $dl2,
    $uu2,
    $z2,
    0

$detail_7_start=[
    {2x6>}{1x2^>}{1y2^}s
    ^{^>}{>}s
]
$detail_7_end={1x2<}{1x4vv>}>s

$chr_7_=
    $detail_7_start,
    $detail_7_end,
    0

# ------------------------------

$d4=v{vvvv}{1x2<}s
$dl4={1x4>vvvv}C
$dd4=[2x3 >{>vvvv}{v}s]
$uc4={3y^}{5x12>^^^^}{3y4^}s
$uu4=[2x3 {^}{^^^^>}{3x2>}s]
$_u2={^^ 1x8>}

# ------------------------------

$chr_13j=
    $s2,
    $dd2,
    $uc2,
    $d4,
    $_u2,
    0

$chr_12_=
    $u2,
    $dl4,
    $uc4,
    $d2,
    0


$chr_11j=
    $u2,
    $d4,
    $_u2,
    0

$detail_16_end={1x2>}{1x8vv>}{1x3<}s

$chr_16j=
    $s2,
    $detail_6_end,
    $detail_16_end,
    $_u2,
    0

$detail_15_end=[.975y$d4!]

$chr_15j=
    $u1,
    $detail_5_mid,
    $detail_15_end,
    $_u2,
    0

$detail_14_mid=[2x3 ^^^]

$chr_14_=
    $u2,
    $dl4,
    $detail_14_mid,
    $detail_4_end,
    0

$detail_19_end=[
    {>}{vvvv1x2>}{1x2<}s
    {1x8>}
]

$chr_19j=
    $s2,
    $dd2,
    $uu2,
    $detail_19_end,
    $_u2,
    0

$chr_18_=
    $u2,
    $dl4,
    $uu4,
    $z2,
    0

$detail_17_end={<}{1x4vvvv<<}{2x3<}s

$chr_17j=
    $detail_7_start,
    $detail_17_end,
    $_u2,
    0


# ------------------------------

$chr_i23_=
    $chr_i_,
    $chr_13j!

$chr_i22_=
    $chr_i_,
    $chr_12_!

$chr_i21_=
    $chr_i_,
    $chr_11j!

$chr_i26_=
    $chr_i_,
    $chr_16j!

$chr_i25_=
    $chr_i_,
    $chr_15j!

$chr_i24_=
    $chr_i_,
    $chr_14_!

$chr_i29_=
    $chr_i_,
    $chr_19j!

$chr_i28_=
    $chr_i_,
    $chr_18_!

$chr_i27_=
    $chr_i_,
    $chr_17j!

# ------------------------------

$acute=(
    $_u2!
    {1y3^ 1x2>}
    M{1z3 >^}C
)
$dot_up=(
    $_u2!
    {1y3^ 1x2>}
    1r8
    1z8
    4:>1l4
)
$bar=(
    $_u2!
    {1y2^ 1x2>}
    3x2>
)
$bar2=(
    $_u2!
    {1y2^ 1x3>}
    >
)

# ------------------------------


$chr_23_=
    $bar,
    $chr_3_!

$chr_22_=
    $dot_up,
    $chr_2_!

$chr_21_=
    $dot_up,
    $chr_1_!

$chr_26_=
    $bar2,
    $chr_6_!

$chr_25_=
    $bar,
    $chr_5_!

$chr_24_=
    $bar2,
    $chr_4_!

$chr_29_=
    $bar,
    $chr_9_!

$chr_28_=
    $bar,
    $chr_8_!

$chr_27_=
    $bar2,
    $chr_7_!

# ------------------------------

$chr_i_=[
    $u2!
    $d2!
]
