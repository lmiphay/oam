# -*- sh -*-

oam_die()
{
    if [[ $(id -u) -eq 0 ]] ; then
	echo "$(oam_ts) $*" | tee -a $OAM_LOGDIR/error.log
    else
	echo "$(oam_ts) $*"
    fi

    exit 1
}

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

oam_logdate()
{
    local logdate=$(ls -1dt $OAM_LOGDIR/2* | head -1)

    if [[ -z "$logdate" ]] ; then
	logdate="$OAM_LOGDIR/$(date +%Y%m%d)"
    fi
    
    echo "$logdate"
}

oam_logphase()
{
    local tag=$1 logfile=$2
    
    sed "s/^/$tag /" | ts $OAM_TS >>$logfile
}

oam_stripansi()
{
    perl -pe 's/\e\[?.*?[\@-~]//g'
}

oam_ts()
{
    date +$OAM_TS
}

oam_version()
{
    echo "1.0"
}
