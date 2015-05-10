# -*- sh -*-

oam_err()
{
    if [[ $(id -u) -eq 0 ]] ; then
	sed "s/^/$1 /" | ts $OAM_TS >>$OAM_LOGDIR/error.log
    else
	sed "s/^/$1 /" | ts $OAM_TS
    fi
}

oam_log()
{
    if [[ $(id -u) -eq 0 ]] ; then
	echo "$(oam_ts) $*" >>$OAM_LOGDIR/oam.log
    else
	echo "$(oam_ts) $*"
    fi
}

oam_stripansi()
{
    perl -pe 's/\e\[?.*?[\@-~]//g'
}

oam_die()
{
    if [[ $(id -u) -eq 0 ]] ; then
	echo "$(oam_ts) $*" | tee -a $OAM_LOGDIR/error.log
    else
	echo "$(oam_ts) $*"
    fi
	
    exit 1
}

oam_ts()
{
    date +$OAM_TS
}
