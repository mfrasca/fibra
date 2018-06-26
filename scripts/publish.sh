#!/bin/sh

# make sure we are in the project root dir
cd $(dirname $0)/..

# make sure you have locally all remote branches
#
git remote update

# let's check what Debian says first
python setup.py sdist | awk 'BEGIN{count=0}/^.*$/{count++; printf("running setup sdist: %d\r", count)}END{printf("\r\n")}'
# debian needs a frozen upstream, on which to base its packaging.  a good
# way to freeze might mean starting a branch at the merge point.

#
TAGNAME=$(ls dist | grep 'tar.gz$' | tail -n1 | sed -e 's/.*\([0-9]\.[0-9]\.[0-9]*\).*/v\1/')
git tag $TAGNAME

# publish on pypi
#
python setup.py sdist --formats zip upload -r pypi

cp dist/ghini.desktop-${PUBLISHING}.tar.gz /tmp/ghini.desktop-${PUBLISHING}.orig.tar.gz
( cd /tmp
  rm -fr ghini.desktop-${PUBLISHING}/ 2>/dev/null
  tar zxf ghini.desktop-${PUBLISHING}.orig.tar.gz 
  cd ghini.desktop-${PUBLISHING}/
  dh_make --yes --indep --file ../ghini.desktop-${PUBLISHING}.orig.tar.gz )
cp debian/* /tmp/ghini.desktop-${PUBLISHING}/debian
( cd /tmp/ghini.desktop-${PUBLISHING}/
  find debian -iname "*.ex" -execdir rm {} \; -or -name "*.source" -execdir rm {} \; -or -name "*~" -execdir rm {} \;
  debuild )
