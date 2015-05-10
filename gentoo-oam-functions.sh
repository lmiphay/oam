# -*- sh -*-

oam_err()
{
    sed "s/^/$1 /" | ts $OAM_TS >>$OAM_LOGDIR/error.log
}

oam_log()
{
    echo "$*" | ts $OAM_TS >>$OAM_LOGDIR/oam.log
}

oam_stripansi()
{
    perl -pe 's/\e\[?.*?[\@-~]//g'
}

oam_die()
{
    echo "$*"
    exit 1
}
