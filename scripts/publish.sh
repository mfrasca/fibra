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
PUBLISHING=$(ls dist | grep 'tar.gz$' | tail -n1 | sed -e 's/.*\([0-9]\.[0-9]\.[0-9]*\).*/\1/')
git tag v$PUBLISHING

# publish on pypi
#
python setup.py sdist --formats zip upload --sign -r pypi

cp dist/fibra-${PUBLISHING}.tar.gz /tmp/fibra_${PUBLISHING}.orig.tar.gz
( cd /tmp
  rm -fr fibra-${PUBLISHING}/ 2>/dev/null
  tar zxf fibra-${PUBLISHING}.orig.tar.gz 
  cd fibra-${PUBLISHING}/ )
cp -a debian /tmp/fibra-${PUBLISHING}
( cd /tmp/fibra-${PUBLISHING}/
  debuild )

echo dput mentors $(ls /tmp/fibra_${PUBLISHING}-*_*.changes | tail -n 1)
