# -*- sh -*-

oam_checknews()
{
    #  [21]     2015-04-16  FFmpeg default
    #  [22]  N  2015-06-08  udev-init-scripts-29 important changes
    eselect news list | egrep '  \[[0-9]*\]  N'
}

oam_cmd()
{
    local logfile=$1

    shift
    oam_log "$*"
    $* >> $logfile 2>&1
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

oam_err()
{
    if [[ $(id -u) -eq 0 ]] ; then
	sed "s/^/$1 /" | ts $OAM_TS >>$OAM_LOGDIR/error.log
    else
	sed "s/^/$1 /" | ts $OAM_TS
    fi
}

oam_indent()
{
    sed -e 's/^/   /'
}

oam_lastdate()
{
    local dir=$(cd $OAM_LOGDIR && ls -1dt 2* | head -1)

    if [[ -z "$dir" ]] ; then
	dir=$(date +%Y%m%d)
    fi

    echo $dir
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

oam_logfile()
{
    if [[ -n "$OAM_LOGDATE" ]] ; then
	local logdate=$OAM_LOGDATE
    else
	local logdate=$(date +%Y%m%d)
	export OAM_LOGDATE=$logdate
    fi

    local logprefix=$OAM_LOGDIR/$logdate

    [[ ! -d $logprefix ]] && mkdir -p $logprefix

    [[ ! -f ${logprefix}/${1}.log ]] && echo "$(oam_ts) created log file" >>${logprefix}/${1}.log

    echo ${logprefix}/${1}.log
}

oam_prevdate()
{
    local laterdate=$1

    (cd $OAM_LOGDIR && ls -d1 20* |grep --before-context=1 $laterdate | head -1)
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
    echo "2.0"
}
