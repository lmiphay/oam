#!/bin/bash

overlay="lmiphay"
overlay_dir="/var/lib/layman/${overlay}"
keywords_dir="/etc/portage/package.keywords"

keywords="${overlay_dir}/oam.keywords"
keywords_link="${keywords_dir}/oam.keywords"

die()
{
    echo $*
    exit 1
}

[ $(id -u) -ne 0 ]                                                && die "please re-run as root, exiting"

[ ! -d "$overlay_dir" ]   && { layman -a "${overlay}"             || die "failed to add ${overlay} overlay"; }

[ ! -d "$keywords_dir" ]                                          && die "please re-run after creating the ${keywords_dir} directory"

[ ! -h "$keywords_link" ] && { ln -s "$keywords" "$keywords_link" || die "failed to symlink oam keywords file: ${keywords_link}"; }

if grep -q 'app-oam' /etc/portage/categories 2>/dev/null; then
    echo "app-oam is already entered into /etc/portage/categories"
else
    echo 'app-oam' >>/etc/portage/categories
fi

exec emerge app-oam/oam
